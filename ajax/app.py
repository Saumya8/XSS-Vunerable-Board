from flask import Flask, render_template, request, redirect, url_for,flash
from flask_wtf import form
import db
import sqlite3
import re
from flask_login import login_user, current_user, logout_user, login_required, LoginManager, UserMixin
from flask import flash
from xml.sax.saxutils import escape, unescape

app=Flask(__name__)

app.config['SECRET_KEY']='c3294467824c35a6751cde802b37198a'
login_manager = LoginManager(app)
login_manager.login_view = "login"


def connect_db():
    db = sqlite3.connect('database.db')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS posts '
                        '(id INTEGER PRIMARY KEY, '
                        'user TEXT, post TEXT)')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS users '
                        '(id INTEGER PRIMARY KEY, '
                        'email TEXT, password TEXT)')
    db.commit()
    return db

def search_posts(input_query):
    posts = db.get_posts()
    result = []
    for (post, user) in posts:
        if re.search(text_str(input_query), text_str(post)) or re.search(text_str(input_query),text_str(user)):
            result.append([ post,user])
    return result

def text_str(input):
    return str(input).lower()




class User(UserMixin):
    #def __init__(self, email, password):
    def __init__(self, *args):
        #super().__init__()
        #self.id = id
        #self.name = name
        if(len(args) == 2):
            self.email = args[0]
            #self.name = args[0]
            self.password = args[1]
            self.authenticated = False
        else:
            self.id = args[0]
            self.email = args[1]
            #self.name = args[1]
            self.password = args[2]
            self.authenticated = False
        self.name = self.email
        #self.name = list({self.email})[0].split('@')[0]
    def is_active(self):
        return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id
    def get_email(self):
        return self.email
    def authenticate(self):
        self.authenticated = True

@login_manager.user_loader
def load_user(id):
   db = connect_db()
   lu = db.cursor().execute("SELECT * from users where id = (?)",(id,)).fetchone()
   if lu is None:
      return None
   else:
        u = User(int(lu[0]), lu[1], lu[2])
        return u




@app.route("/", methods=['GET', 'POST'])
def login():
    # print(request.environ['REMOTE_ADDR'])
    # print(request.remote_addr)
    if current_user.is_authenticated:
        flash("Oops. Already Logged in. Logout First")
        return redirect(url_for('search'))

    if request.method=='POST':
        db = connect_db()
        currEmail=db.cursor().execute('SELECT * FROM users where email=(?)',(request.form['email'],)).fetchone()
        if currEmail is None:
            flash("Email entered isn't registered yet. Click on register")
            print("Unregistered Email")
            
        else:
            user = list(currEmail)
            Us = load_user(user[0])
            if(request.form['email'] == Us.email) and request.form['password'] == Us.password:
                login_user(Us)
                print("login Successfull")
                redirect(url_for('search'))
            else:
                print("login unsuccessful")
                flash('Unsuccessful Login. Wrong password')
    return render_template('login.html')
    


@app.route("/signup", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = connect_db()
        if db.cursor().execute('SELECT email FROM users where email=(?)',(request.form['email'],)).fetchone() is None:
            db.cursor().execute('INSERT INTO users (email, password) '
                                'VALUES (?, ?)', (request.form['email'],request.form['password'],))
            db.commit()
            print("User added successfully")
            return redirect(url_for('login'))
        else:
            print("user exists already")
    return render_template('signup.html')

@app.route("/profile")
@login_required
def success():
    if current_user.is_authenticated:
        print("logged into Profile")
        return render_template('profile.html')
    else:
        return render_template('login.html')



@app.route("/search")
@login_required
def search():
    input_query=request.args.get('input')
    unfiltered_posts = db.get_posts()
    print(unfiltered_posts)
    if input_query:
        posts=search_posts(escape(input_query))
        print("escaped data")
        print(escape(input_query))
        return render_template('search.html', search_query=escape(input_query),posts=posts)
    return render_template('search.html', search_query=input_query)



@app.route("/posts", methods=['GET', 'POST'])
@login_required
def c():
    if request.method == 'POST':
        post=escape(request.form['post'])
        print("escaped post:")
        print(post)
        db.add_post(post,current_user.email.split('@')[0])
    posts = db.get_posts()
    # print(request.remote_addr)
    print(posts)
    print(type(posts))
    return render_template('posts.html',posts=posts)

@app.route("/logout")
@login_required
def logout():
    print("on logout page")
    if(current_user.is_authenticated):
        logout_user()
        print("user logged out")
        
   
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run()
        
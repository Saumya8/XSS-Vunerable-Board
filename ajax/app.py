#from db import add_user
from flask import Flask, render_template, request, url_for,redirect, flash, Response 
import db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
#from forms import LoginForm
#from forms import LoginForm

app=Flask(__name__)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.route("/")
def search():
    input_query=request.args.get('input')
    return render_template('search.html', search_query=input_query)


@app.route("/posts", methods=['GET', 'POST'])
def c():
    if request.method == 'POST':
        db.add_post(request.form['post'])
    posts = db.get_posts()
    return render_template('posts.html',posts=posts)

@app.route("/profile")
def success():
    if current_user.is_authenticated:
        print("logged into Profile")
        return render_template('profile.html')
    else:
        flash("First login")
        return render_template('login.html')

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
def load_user(user_id):
   conn = sqlite3.connect('database.db')
   curs = conn.cursor()
   curs.execute("SELECT * from users where user_id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
        u = User(int(lu[0]), lu[1], lu[2])
        #u.authenticate()
        return u 

@app.route('/logout')
@login_required
def logout():
    print("on logout page")
    if(current_user.is_authenticated):
        logout_user()
        print("loggout")
        flash("Logout successful. Login again")
    else:
        print("not logged in")
        flash("You need to login first.")
    return redirect(url_for('login'))

@app.route("/signup", methods=['GET','POST'])
def signup():
    print("start signup")
    if request.method == 'POST':
        db.connect()
        #creating a default email for non-null
        email = "S"; password ="S"; print("input start")
        email = request.form['username']
        password = request.form['password'];    print("got input")
        conn = sqlite3.connect('database.db');  print("db successfully loaded!")
        curs = conn.cursor()
        curs.execute("SELECT email FROM users where email = (?)",[email])
        valemail = curs.fetchone();             print("fetched user")
        if valemail is not None:
            print("user already exists")
            flash('This Email ID is already registered. Please use login')
        elif email != "S" and password != "S":
            #db.add_user(email, password)
            #new_user = User(email=email, password=password)#password=generate_password_hash(password, method='sha256'))
            conn.execute('INSERT OR IGNORE INTO users (email, password) VALUES(?,?)', (email,password)); conn.commit()
            print("user added"); flash('Signup successfully '+ str(email) + '. Now Login')
            return redirect(url_for('login'))
        else:
            flash('Signup unsuccessfully, email or password is blank'); print("signup failed")
        #new_user = User(email='xyz@gmail.com', password='xyz123')#password=generate_password_hash('password', method='sha256'))
        #db.session.add(new_user); db.session.commit()
    else:
        print("not post?")
        #return render_template('signup.html')
    return render_template('signup.html')

@app.route("/login", methods=['GET','POST'])
def login():
    
    #db.add_user('xyz@gmail.com', 'xyz123')
    if current_user.is_authenticated:
        flash("Oops. Already Logged in. Logout First")
        return redirect(url_for('search'))

    if request.method == 'POST':
        db.connect()
        print("take input")
        email = request.form['username']
        password = request.form['password']
        #print(request.form.get('remember'))
        rem = request.form.get('remember')
        if rem is not None:
            remember = True
        else:
            remember = False
        #print(remember)
        print("got input")

        conn = sqlite3.connect('database.db');          print("db loaded")
        curs = conn.cursor()
        curs.execute("SELECT * FROM users where email = (?)",[email])
        valemail = curs.fetchone()
        if valemail is None:
            flash("Email entered isn't registered yet. Click on register")
            print("Unregistered Email")
            #raise ValidationError('This Email ID is not registered. Please register before login')
        else:
            user = list(valemail)
            Us = load_user(user[0])
            #check_password_hash(user.password, password) #for hashing
            if(email == Us.email) and password == Us.password:
                login_user(Us, remember=remember)
                print("login Successfull")
                Umail = list({email})[0].split('@')[0]
                flash('Logged in successfully '+Umail)
                redirect(url_for('search'))
            else:
                print("login unsuccessfull")
                flash('Login Unsuccessfull. Wrong password')
    return render_template('login.html',title='Login')


if __name__ == "__main__":
    app.run()
        

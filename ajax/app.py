from flask import Flask, render_template, request, redirect, flash
from flask.helpers import url_for
from flask_login import login_user, current_user, logout_user, login_required, LoginManager, UserMixin
#from flask import Flask 
#import logging
import logging
import db

adminU = { 0:5, 1:'admin', 2:'xss1234'}


app=Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = "login"
app.config['SECRET_KEY']='c3294467824c35a6751cde802b37198a'



class User(UserMixin):
    def __init__(self, *args):
        #if(len(args) == 2):
            #self.email = args[0]
            #self.password = args[1]
            #self.authenticated = False
        #else:
        self.id = args[0]
        self.email = args[1]
        self.password = args[2]
        self.authenticated = False
        #self.name = self.email;
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
    return User(id,adminU[1], adminU[2])
   #lu = [username, password]
   #lu = dby.cursor().execute("SELECT * from users where id = (?)",(id,)).fetchone()
   #if lu is None:
      #return None
   #else:
        #u = User( lu[1], lu[2])
        #return u

@app.route("/", methods=['GET', 'POST'])
def register():
    email=request.args.get('email')
    password=request.args.get('password')
    #users = db.get_users()
    if email is not None and password is not None:
        db.add_user(email,password)
        return redirect(url_for('data'))
    return render_template('login.html')

@app.route("/admin", methods=['GET','POST'])
def admin():
    print("opened admin")
    if current_user.is_authenticated:
        print("Already Logged in")
        return redirect(url_for('data'))
    if request.method=='POST':
        username = request.form['email']
        password = request.form['password']
        if username is None or password is None: 
            flash("Enter all the Fields")
            print("Fields Empty.")
            
        else:
            Us = load_user(adminU[0])
            if(str(username) == Us.email) and (str(password) == Us.password):
                login_user(Us)
                #User(username, password)
                print("login Successfull")
                return redirect(url_for('data'))
            else:
                print("login unsuccessful")
                flash('Unsuccessful Login. Wrong password')
    return render_template('admin_login.html')

@app.route("/logout")
@login_required
def logout():
    print("on logout page")
    if(current_user.is_authenticated):
        logout_user()
        print("user logged out")
        
   
    return redirect(url_for('admin'))


@app.route("/data")
def data():
    if current_user.is_authenticated:
        #flash("Oops. Already Logged in. Logout First")
        users=db.get_users()
        return render_template('attack.html',users=users)
    else:
        flash("Login First")
        return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
    #logging.basicConfig(filename='demo.log', level=logging.DEBUG)
        
from _typeshed import NoneType
from flask import Flask, render_template, request, redirect, url_for,flash
import db
from flask_login import login_user, current_user, logout_user, login_required
from _typeshed import NoneType


app=Flask(__name__)

app.config['SECRET_KEY']='c3294467824c35a6751cde802b37198a'


    


@app.route("/", methods=['GET', 'POST'])
def register():
    email=request.args.get('email')
    password=request.args.get('password')
    if email is not None & password is not None:
        db.add_user(request.form['email'],request.form['password'])
        return "Boom!"
    return render_template('login.html')





if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
        
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import db



app=Flask(__name__)

app.config['SECRET_KEY']='c3294467824c35a6751cde802b37198a'


    


@app.route("/", methods=['GET', 'POST'])
def register():
    email=request.args.get('email')
    password=request.args.get('password')
    users=db.get_users()
    if email is not None and password is not None:
        db.add_user(email,password)
        return redirect(url_for('data'))
    return render_template('login.html')


@app.route("/data")
def data():
    users=db.get_users()
    return render_template('attack.html',users=users)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
        
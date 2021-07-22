from flask import Flask, render_template, request, redirect, url_for
import db
from flask_login import login_user, current_user, logout_user, login_required
app=Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('posts'))
    # if request.method == 'POST':
    #     db.verify_user(request.form['username'],request.form['password'])
    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('posts'))
    if request.method == 'POST':
        db.add_user(request.form['username'],request.form['password'])
    return render_template('sign_up.html')

@app.route("/search")
def search():
    input_query=request.args.get('input')
    return render_template('search.html', search_query=input_query)



@app.route("/posts", methods=['GET', 'POST'])
def c():
    if request.method == 'POST':
        db.add_post(request.form['post'])
    posts = db.get_posts()
    print(request.remote_addr)
    return render_template('posts.html',posts=posts)



if __name__ == "__main__":
    app.run()
        
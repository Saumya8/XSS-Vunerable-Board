from flask import Flask, render_template, request
import db

app=Flask(__name__)




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



if __name__ == "__main__":
    app.run()
        
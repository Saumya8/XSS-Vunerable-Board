from flask import Flask, render_template, request
import db

app=Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    input_query=request.args.get('input')
    comments = db.get_comments(input_query)

    if request.method == 'POST':
        db.add_comment(input_query)



    return render_template('index.html', 
    comments = comments,
    search_query=input_query)
    




if __name__ == "__main__":
    app.run()
        
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")
def index():
    input_query=request.args.get('input')
    return render_template('index.html', search_query=input_query)
    




if __name__ == "__main__":
    app.run()
        
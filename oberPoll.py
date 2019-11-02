from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Akshat')
def akshat():
    return "<h1> Henry sucks!</h1>"

if __name__ == "__main__":
    app.run(debug=True)

from flask import *

#SQLAlchemy- -Database
#https://www.youtube.com/watch?v=QjtW-wnXlUY -- Tutorial

app = Flask(__name__)
#db=SQLAlchemy(app)

@app.route('/')
def index():
    # id = db.Column('id', db.Integer, primary_key=True)
    # name = db.Column('name', db.String)
    # db.add({"name":"Akshat"})
    # db.commit()
    # print(db.query(1))
    return render_template("index.html")

@app.route('/Akshat')
def akshat():
    return "<h1> Henry sucks!</h1>"

if __name__ == "__main__":
    app.run(debug=True)

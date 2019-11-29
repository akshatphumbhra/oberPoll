from flask import *
from models import db, Users, Polls, Topics, Options, UserPolls
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

oberPoll = Flask(__name__)

#Loading config from config.py
oberPoll.config.from_object('config')

db.init_app(oberPoll)
db.create_all(app=oberPoll)

migrate = Migrate(oberPoll, db, render_as_batch=True)

@oberPoll.route('/')
def home():
    return render_template('index.html')

@oberPoll.route('/signup', methods=['GET','POST'])
def signup():
    #if Post
    if request.method == 'POST':
        #Get details from form
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        #Hash password for security
        password = generate_password_hash(password)

        user = Users(email=email, username=username, password=password)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations! Your account has been created! Please login.')

        return redirect(url_for('home'))

    #Render the template if its a GET request
    return render_template('signup.html')
# class index():
#      id = db.Column(db.Integer, primary_key=True, unique=true, nullable=true) #does true and false need to be True and False
#      name = db.Column(db.String(20), unique=true, nullable = false)
#     # db.add({"name":"Akshat"})
#     # db.commit()
#     # print(db.query(1))
#     return render_template("index.html")

@oberPoll.route('/favicon.ico')
def test():
    return "This sucks!"

@oberPoll.route('/login', methods =['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    user = Users.query.filter_by(username=username).first()

    if user:
        password_hash = user.password

        if check_password_hash(password_hash, password):
            session['user'] = username

            flash('Login was successful! Yay!')

    else:
        flash('Username or password was incorrect. Please try again.', 'error')

    return redirect(url_for('home'))

@oberPoll.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')

        flash('You have successfully been logged out!')

    return redirect(url_for('home'))

@oberPoll.route('/polls', methods=['GET'])
def createPoll():
    return render_template('createpoll.html')

@oberPoll.route('/polls/<poll_name>')
def poll():
    return render_template('index.html')

if __name__ == "__main__":
    oberPoll.run()

# -- ---
# -- Globals
# -- ---
#
# -- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
# -- SET FOREIGN_KEY_CHECKS=0;
#
# -- ---
# -- Table 'User'
# --
# -- ---
#
# DROP TABLE IF EXISTS `User`;
#
# CREATE TABLE `User` (
#   `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
#   `Name` VARCHAR(64) NULL DEFAULT NULL,
#   `Paassword` VARCHAR(64) NULL DEFAULT NULL,
#   `Student?` BINARY(8) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`)
# );
#
# -- ---
# -- Foreign Keys
# -- ---
#
#
# -- ---
# -- Table Properties
# -- ---
#
# -- ALTER TABLE `User` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
#
# -- ---
# -- Test Data
# -- ---
#
# -- INSERT INTO `User` (`id`,`Name`,`Paassword`,`Student?`) VALUES
# -- ('','','','');

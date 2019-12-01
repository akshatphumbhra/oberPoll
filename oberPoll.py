from flask import *
from models import db, Users, Polls, Topics, Options, UserPolls
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime
from config import SQLALCHEMY_DATABASE_URI

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

@oberPoll.route('/api/poll/<poll_name>')
def api_poll(poll_name):
    poll = Topics.query.filter(Topics.title.like(poll_name)).first()

    return jsonify({'Polls': [poll.to_json()]}) if poll else jsonify({'message': 'poll not found'})

#Add and receive polls from or to the database
@oberPoll.route('/api/polls', methods=['GET', 'POST'])
def api_polls():

    if request.method == 'POST':

        #Get poll and save in the database
        poll = request.get_json()

        for key, value in poll.items():
            if not value:
                return jsonify({'message': 'value for {} is empty'.format(key)})

        title = poll['title']
        options_query = lambda option: Options.query.filter(Options.name.like(option))
        options = [Polls(option=Options(name=option))
                        if options_query(option).count() == 0
                        else Polls(option=options_query(option).first()) for option in poll['options']]

        #eta = datetime.utcfromtimestamp(poll['close_date'])
        new_topic = Topics(title=title, options=options)#, close_date=eta)

        db.session.add(new_topic)
        db.session.commit()

        #from tasks import close_poll

        #close_poll.apply_async((new_topic.id, SQLALCHEMY_DATABASE_URI), eta=eta)
        return jsonify({'message': 'Poll was successfully cretaed!'})

    else:
        #Query the database and return all polls as JSON objects
        polls= Topics.query.join(Polls).order_by(Topics.id.desc()).all()
        all_polls ={'Polls': [poll.to_json() for poll in polls]}


        return jsonify(all_polls)

@oberPoll.route('/api/polls/options')
def api_polls_options():
    all_options = [option.to_json() for option in Options.query.all()]

    return jsonify(all_options)

@oberPoll.route('/api/poll/vote', methods=['PATCH'])
def api_poll_vote():
    # poll = request.get_json()
    #
    # poll_title, option = (poll['poll_title'], poll['option'])
    #
    # join_tables = Polls.query.join(Topics).join(Options)
    #
    #  # Get topic and username from the database
    # topic = Topics.query.filter_by(title=poll_title, status=True).first()
    # user = Users.query.filter_by(username=session['user']).first()
    # # if poll was closed in the background before user voted
    # if not topic:
    #     return jsonify({'message': 'Sorry! this poll has been closed'})
    #
    # # filter options
    # option = join_tables.filter(Topics.title.like(poll_title), Topics.status == True).filter(Options.name.like(option)).first()
    #
    # # check if the user has voted on this poll
    # poll_count = UserPolls.query.filter_by(topic_id=topic.id).filter_by(user_id=user.id).count()
    # if poll_count > 0:
    #     return jsonify({'message': 'Sorry! multiple votes are not allowed'})
    #
    # if option:
    #     # record user and poll
    #     user_poll = UserPolls(topic_id=topic.id, user_id=user.id)
    #     db.session.add(user_poll)
    #
    #     # increment vote_count by 1 if the option was found
    #     option.vote_count += 1
    #     db.session.commit()
    #
    #     return jsonify({'message': 'Thank you for voting!'})
    #
    # return jsonify({'message': 'Option or poll was not found. Please try again'})
    poll = request.get_json()

    poll_title, option = (poll['poll_title'], poll['option'])

    join_tables = Polls.query.join(Topics).join(Options)
    # filter options
    option = join_tables.filter(Topics.title.like(poll_title)).filter(Options.name.like(option)).first()

    # increment vote_count by 1 if the option was found
    if option:
        option.vote_count += 1
        db.session.commit()

        return jsonify({'message': 'Thank you for voting'})

    return jsonify({'message': 'option or poll was not found please try again'})

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

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

#Home page
@oberPoll.route('/')
def home():
    return render_template('index.html')

#Signing up user
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

#Exists for no real reason
@oberPoll.route('/favicon.ico')
def test():
    return "This sucks!"

#Logs user in
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

#Logs user out
@oberPoll.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')

        flash('You have successfully been logged out!')

    return redirect(url_for('home'))

#Redirects to createpoll.html
@oberPoll.route('/polls', methods=['GET'])
def createPoll():
    return render_template('createpoll.html')

#Redirects back to index as all polls show up there
@oberPoll.route('/polls/<poll_name>')
def poll():
    return render_template('index.html')

#API endpoint that returns JSON object for specific poll (poll_name = title)
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


        new_topic = Topics(title=title, options=options)

        db.session.add(new_topic)
        db.session.commit()

        return jsonify({'message': 'Poll was successfully cretaed!'})

    else:
        #Query the database and return all polls as JSON objects
        polls= Topics.query.join(Polls).order_by(Topics.id.desc()).all()
        all_polls ={'Polls': [poll.to_json() for poll in polls]}


        return jsonify(all_polls)

#Api end point that returns all options
@oberPoll.route('/api/polls/options')
def api_polls_options():
    all_options = [option.to_json() for option in Options.query.all()]

    return jsonify(all_options)

#Api endpoint for voting
@oberPoll.route('/api/poll/vote', methods=['PATCH'])
def api_poll_vote():

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

from oberPoll import oberPoll, db
from multiprocessing import Process
import requests
import os
import time


class TestOberPoll():

    @classmethod
    def setUpClass(cls):
        oberPoll.config['DEBUG'] = False
        oberPoll.config['TESTING'] = True
        cls.DB_PATH = os.path.join(os.path.dirname(__file__), 'oberPoll_test.db')
        oberPoll.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(cls.DB_PATH)
        cls.hostname = 'http://localhost:7000'
        cls.session = requests.Session()

        with oberPoll.app_context():
            db.init_app(oberPoll)
            db.create_all()
            cls.p = Process(target=oberPoll.run, kwargs={'port': 7000})
            cls.p.start()
            time.sleep(2)

        # create new poll
        poll = {"title": "Flask vs Django",
                "options": ["Flask", "Django"],
                "close_date": 1581556683}
        requests.post(cls.hostname + '/api/polls', json=poll).json()

        # create new admin user
        signup_data = {'email': 'admin@gmail.com', 'username': 'Administrator',
                       'password': 'admin'}
        requests.post(cls.hostname + '/signup', data=signup_data).text

    def setUp(self):
        self.poll = {"title": "who's the fastest footballer",
                     "options": ["Hector bellerin", "Gareth Bale", "Arjen robben"],
                     "close_date": 1581556683}

    def test_new_user(self):
        signup_data = {'email': 'user@gmail.com', 'username': 'User',
                       'password': 'password'}

        result = requests.post(self.hostname + '/signup', data=signup_data).text

        print(result)

        assert 'Congratulations! Your account has been created! Please login' in result

    def test_login(self):

        # Login data
        data = {'username': 'Administrator', 'password': 'admin'}
        result = self.session.post(self.hostname + '/login', data=data).text

        assert 'Create a poll' in result

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.DB_PATH)
        cls.p.terminate()

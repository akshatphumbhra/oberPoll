#Configuration file
import os
basedir = os.path.join(os.path.dirname(__file__), 'oberPoll.db')
SECRET_KEY = 'password'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(basedir)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

# class Config(object):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'app.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

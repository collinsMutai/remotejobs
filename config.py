import os

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:7749@localhost:5432/jobs"

SQLALCHEMY_TRACK_MODIFICATIONS = False



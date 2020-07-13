import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgres://admin:secret@192.168.99.100:5432/appdb'

from flask import Flask
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['DATABASE'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'spacexplorer.db'))

from spaceapp import routes

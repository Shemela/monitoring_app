import os

from flask import Flask
from monitoring.views.base import IndexView

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('flask.conf.py')

app.root_path = os.path.join(app.root_path, 'monitoring')

app.add_url_rule('/', view_func=IndexView.as_view('index'))

app.debug = True

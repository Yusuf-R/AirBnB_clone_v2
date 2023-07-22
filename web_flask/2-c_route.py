#!/usr/bin python3
"""This script will start a flask application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def index_hbnb():
    """displays HBNB!"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def index_c_text(text):
    """displays C followed by the value of the text variable"""
    return 'C {}'.format(text.replace("_", " "))


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)

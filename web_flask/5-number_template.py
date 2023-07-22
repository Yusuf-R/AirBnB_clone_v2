#!/usr/bin/python3
"""This script will start a flask application"""

from flask import Flask
from flask import render_template

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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def index_python_text(text):
    """Display 'Python ', followed by the value of the text variable"""
    return 'Python {}'.format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def index_number_n(n):
    """displays n is a number"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def index_num_template(n):
    """display a HTML page only if n is an integer"""
    return (render_template('5-number.html', num=n))


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)

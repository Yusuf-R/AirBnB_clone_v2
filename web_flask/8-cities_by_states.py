#!/usr/bin/python3
"""script that lists all cities from a given state"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays all the state to the html pages"""
    all_states = storage.all(State).values()
    return render_template('7-states_list.html', states=all_states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """lists all cities from a given state"""
    all_states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=all_states)


@app.teardown_appcontext
def teardown(error):
    """teardown the databse session"""
    storage.close()


if __name__ == "__main__":
    """start the application"""
    app.run(host='0.0.0.0', port=5000)

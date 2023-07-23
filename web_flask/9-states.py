#!/usr/bin/python3
"""script that lists all cities from a given state"""
from os import stat
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_by_state(id):
    """lists all cities from a given state"""
    all_states = storage.all(State).values()

    if not id:
        return render_template('9-states.html',
                               match_state=None,
                               states=all_states)

    for state in all_states:
        if state.id == id:
            return render_template('9-states.html',
                                   match_state=state,
                                   states=None)
    return render_template('9-state.html',
                           match_state=None,
                           states=None)


@app.teardown_appcontext
def teardown(error):
    """teardown the databse session"""
    storage.close()


if __name__ == "__main__":
    """start the application"""
    app.run(host='0.0.0.0', port=5000)

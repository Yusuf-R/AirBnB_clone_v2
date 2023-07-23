#!/usr/bin/python3
"""List all the states in the DB in HTML""""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a list of states in html"""
    from models.state import State
    all_states = storage.all(State).values()
    return render_template('7-states_list.html', states=all_states)


@app.teardown_appcontext
def close_db(error):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    """Start the Flask app"""
    app.run(host="0.0.0.0", port=5000)

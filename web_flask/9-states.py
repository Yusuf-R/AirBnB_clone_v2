#!/usr/bin/python3
"""script that lists all cities from a given state"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_by_state(id):
    """lists all cities from a given state"""
    all_states = storage.all(State).values()
    st_id = None
    if id:
        st_id = "State." + id
    return render_template('9-states.html', st_db=all_states, st_id=st_id)


@app.teardown_appcontext
def teardown(error):
    """teardown the databse session"""
    storage.close()


if __name__ == "__main__":
    """start the application"""
    app.run(host='0.0.0.0', port=5000)

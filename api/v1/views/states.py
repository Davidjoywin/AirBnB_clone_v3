#!/usr/bin/python3
"""the states veiws page"""
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/', methods=['GET'])
def list_states():
    """returns list of states"""
    states_all = []
    state_all_objs = storage.all("State").values()
    for state_obj in state_all_objs:
        states_all.append(state_obj.to_dict())
    return jsonify(states_all)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object'''
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a State'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a State object'''
    state = storage.get(State, state_id)
    if state:
        req = request.get_json()
        if not req:
            abort(400, 'Not a JSON')
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
    abort(404)

#!/usr/bin/python3
"""the cities view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def list_cities_of_state(state_id):
    '''Returns  all City'''
    all_states = storage.all("State").values()
    state_obj = []
    for obj in all_states:
        if obj.id == state_id:
            state_obj.append(obj.to_dict())
    if not state_obj:
        abort(404)
    cities_list = []
    for obj in storage.all("City").values():
        if state_id == obj.state_id:
            cities_list.append(obj.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''Retrieves a City object'''
    all_cities = storage.all("City").values()
    city_obj = None
    for obj in all_cities:
        if obj.id == city_id:
            city_obj = obj.to_dict()
            break
    if not city_obj:
        abort(404)
    return jsonify(city_obj)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Deletes a City object'''
    all_cities = storage.all("City").values()
    city_obj = None
    for obj in all_cities:
        if obj.id == city_id:
            city_obj = obj
            break
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    '''Edits a City object'''

    all_cities = storage.all("City").values()
    city_dict = {}
    for obj in all_cities:
        if obj.id == city_id:
            city_dict = obj.to_dict()
            break
    if not city_dict:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    city_dict['name'] = request.json['name']
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(city_dict), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    '''Creates a City'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_states = storage.all("State").values()
    state_obj = []
    for obj in all_states:
        if obj.id == state_id:
            state_obj.append(obj.to_dict())
    if state_obj == []:
        abort(404)
    cities = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dict())
    return jsonify(cities[0]), 201

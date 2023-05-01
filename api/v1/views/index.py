#!/usr/bin/python3
"""returns  JSON: "status": OK"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import text


@app_views.route('/stats', methods=['GET'])
def stats():
    counts = {
            'amenities': storage.count(text('Amenity')),
            'cities': storage.count(text('City')),
            'places': storage.count(text('Place')),
            'reviews': storage.count(text('Review')),
            'states': storage.count(text('State')),
            'users': storage.count(text('User'))
                                                                    }
    return jsonify(counts)


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'OK'
        })

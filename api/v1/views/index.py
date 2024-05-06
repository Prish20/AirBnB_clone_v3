#!/usr/bin/python3
"""
This module provides endpoints for the AirBnB project API.

It includes:
- A Flask blueprint instance
- A route that returns the API status in JSON format
- A route that returns the count of each object type in JSON format
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Returns the number of each object type"""
    stats = {
        "Amenity": storage.count(Amenity),
        "City": storage.count(City),
        "Place": storage.count(Place),
        "Review": storage.count(Review),
        "State": storage.count(State),
        "User": storage.count(User)
    }
    return jsonify(stats)

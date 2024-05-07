#!/usr/bin/python3
"""
This module provides a RESTful API for Place objects.
"""

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json(force=True)
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    place = Place(city_id=city_id, **data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json(force=True)
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects based on the JSON body of the request"""
    all_places = storage.all(Place).values()
    data = request.get_json()

    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # If the JSON body is empty or all keys are empty, return all Place objects
    if not data or all(not data.get(key) for key in
                       ["states", "cities", "amenities"]):
        return jsonify([place.to_dict() for place in all_places])

    # Get list of places based on states and cities
    places = set()
    if "states" in data:
        for state_id in data["states"]:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        places.add(place)
    if "cities" in data:
        for city_id in data["cities"]:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    places.add(place)

    # Filter places based on amenities
    if "amenities" in data:
        amenities = set(storage.get(Amenity,
                                    amenity_id) for amenity_id
                        in data["amenities"])
        places = [place for place in places if
                  amenities.issubset(set(place.amenities))]

    return jsonify([place.to_dict() for place in places])

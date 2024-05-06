#!/usr/bin/python3
"""
This module provides the status endpoint for the AirBnB project API.

It includes:
- A Flask blueprint instance
- A route that returns the API status in JSON format
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

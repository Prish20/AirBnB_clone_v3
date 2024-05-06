#!/usr/bin/python3
"""
This module defines a Flask application to manage the AirBnB project API.

It provides:
- A Flask application instance
- Blueprint registration for different routes
- Teardown handling for closing the database session
- Error handling for 404 errors in JSON format
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response"""
    response = {
        "error": "Not found"
    }

    return make_response(jsonify(response), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)

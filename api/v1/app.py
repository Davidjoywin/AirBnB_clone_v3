#!/usr/bin/python3
"""register the blueprint app_views to your Flask
    instance app
    declare a method to handle
    @app.teardown_appcontext that
    calls storage.close()
"""
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """returns a 404 page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """close the storage"""
    storage.close()


if __name__ == "__main__":
    import os

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)

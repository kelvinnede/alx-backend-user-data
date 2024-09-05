#!/usr/bin/env python3
"""API entry point"""
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)

auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()

@app.before_request
def before_request():
    """ Before each request """
    if auth:
        request.current_user = auth.current_user(request)

@app.errorhandler(404)
def not_found(error):
    """ 404 Not Found handler """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    """ 401 Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """ 403 Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)


#!/usr/bin/env python3
""" App module to test simple user authentication application
"""
from flask import (Flask, jsonify, request)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """ Respond with a JSON data """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """ Register a new user """
    user_email = request.form['email']
    user_password = request.form['password']
    try:
        AUTH.register_user(user_email, user_password)
        response = (jsonify({"email": user_email, "message": "user created"}), 200)
    except ValueError:  # User is already registered
        response = (jsonify({"message": "email already registered"}), 400)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

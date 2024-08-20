#!/usr/bin/env python3
""" App module to test simple user authentication application
"""
from flask import (
        Flask, jsonify, request, make_response,
        abort, redirect, url_for
        )
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """ Respond with a JSON data """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """ Registers a new user """
    user_email = request.form["email"]
    user_password = request.form["password"]
    try:
        AUTH.register_user(user_email, user_password)
        response = (
                jsonify({"email": user_email, "message": "user created"}),
                200
            )
    except ValueError:  # User is already registered
        response = (
                jsonify({"message": "email already registered"}),
                400  # Bad request
            )
    return response


@app.route("/sessions", methods=["POST"])
def login():
    """ Verify a user and creates a login session
    """
    user_email = request.form["email"]
    user_password = request.form["password"]
    if AUTH.valid_login(user_email, user_password):
        session_id = AUTH.create_session(user_email)
        payload = {"email": user_email, "message": "logged in"}
        response = make_response(jsonify(payload))
        response.set_cookie("session_id", session_id)
    else:
        abort(401)  # Unauthorized: access denied
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """ Destroys user's session and redirects user to home ('/') page
    """
    session_id = request.cookies.get('session_id')
    if session_id == None:
        session_id = ""  # To avoid retrieving user's with empty session field
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
    else:
        abort(403)  # Forbidden
    return redirect(url_for('home'))


@app.route("/profile")  # Method = GET
def profile():
    """ Retrieves user's profile information
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        payload = {"email": user.email}
    else:
        abort(403)  # Forbidden
    return jsonify(payload)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """ Retrieves user's reset password token given email from form data
    """
    user_email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(user_email)
    except ValueError:  # Email not registered
        abort(403)  # Forbidden
    else:  # Email is registered
        payload = {"email": user_email, "reset_token": reset_token}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

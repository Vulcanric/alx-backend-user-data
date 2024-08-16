#!/usr/bin/env python3
""" App module to test simple user authentication application
"""
from flask import (Flask, jsonify)
app = Flask(__name__)


@app.route("/")
def index():
    """ Respond with a JSON data """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

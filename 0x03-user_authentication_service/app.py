#!/usr/bin/env python3
'''basic flask app'''
from flask import Flask, jsonify
from auth import Auth
from db import DB

app = Flask(__name__)
db = DB()
auth = Auth()


@app.route('/', methods=['GET'])
def index():
    '''basic index route'''
    return jsonify("message": "Bienvenue")


if __name__ = "__main__":
    app.run(host='0.0.0..0', port='5000')

#!/usr/bin/env python3
'''basic flask app'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index() -> str:
    '''basic index route'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    '''users endpoint'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registerd"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    '''login function'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    '''logout function'''
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    '''profile function'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password() -> str:
    '''resets password'''
    email = request.get('email')
    user = self._db.find_user_by(email=email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_token(email)
        return jsonify({"email": user.email, "reset_token": token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

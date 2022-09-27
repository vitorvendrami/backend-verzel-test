import json

from flask import  request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required, JWTManager

from app import app, csrf
from models.UserModel import Users


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@app.route('/token', methods=["POST"])
@csrf.exempt
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = Users.query.filter_by(email=email).first()
    if not user or password != user.password:
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)

    response = {"access_token": access_token}
    return response


@app.route("/logout", methods=["POST"])
@csrf.exempt
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

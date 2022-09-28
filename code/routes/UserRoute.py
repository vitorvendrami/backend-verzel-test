from flask import Response, request
from flask_jwt_extended import jwt_required

from app import app, db, csrf
from handlers.ResponseHandler import ResponseHandler as rp
from models.UserModel import Users

from services.UserService import UserService

users_model = Users


@app.route('/user/<id>', methods=["get"])
@jwt_required()
def get_user(id: int) -> Response:
    """Retriev User by id"""
    user_json = UserService.return_user_by_id(id)
    return rp.generate_basic_response(content_value=user_json)


@app.route("/user/register", methods=["POST"])
@csrf.exempt
def register_user() -> Response:
    """User Creation Route"""
    body = request.get_json()
    created, user = UserService.create_user(**body)

    if created:
        return rp.generate_basic_response(user, status=201, message="Criado com sucesso")

    return rp.generate_default_400_response()

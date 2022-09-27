from flask import Response, request
from flask_jwt_extended import jwt_required

from app import app, csrf
from handlers.ResponseHandler import ResponseHandler as rp
from services.CarsService import CarsService


@app.route('/cars', methods=["get"])
@jwt_required()
def get_all_cars() -> Response:
    cars_json = CarsService.return_all_cars()
    return rp.generate_basic_response(content_value=cars_json)


@app.route('/cars/<id>', methods=["get"])
@jwt_required()
def get_car_by_id(id):
    cars_json = CarsService.filter_car_by_id(id)
    return rp.generate_basic_response(content_value=cars_json.to_json())


@app.route("/cars", methods=["POST"])
@csrf.exempt
@jwt_required()
def register_car():
    body = {
        "name": request.form.get("name", None),
        "brand": request.form.get("brand", None),
        "model": request.form.get("model", None),
        "file": request.files["file"],
    }

    created, car = CarsService.create_car(**body)

    if created:
        return rp.generate_basic_response(car, status=201, message="Criado com sucesso")

    return rp.generate_default_400_response()


@csrf.exempt
@jwt_required()
@app.route("/cars/<id>", methods=["PUT"])
def update_car(id):
    body = {
        "name": request.form.get("name", None),
        "brand": request.form.get("brand", None),
        "model": request.form.get("model", None),
        "file": request.files["file"],
    }
    #
    cars_json = CarsService.update_car_instance_by_id(id, **body)
    return rp.generate_basic_response(content_value=cars_json)


@csrf.exempt
@jwt_required()
@app.route("/cars/<id>", methods=["DELETE"])
def delete_car(id):
    cars_json = CarsService.delete_cat_instance_by_id(id)
    return rp.generate_basic_response(content_value=cars_json)

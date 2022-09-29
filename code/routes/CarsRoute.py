from flask import Response, request
from flask_jwt_extended import jwt_required

from app import app, csrf
from handlers.ResponseHandler import ResponseHandler as rp
from services.CarsService import CarsService


@app.route("/cars", methods=["get"])
def get_all_cars() -> Response:
    cars_json = CarsService.return_all_cars_ordered_by_price()
    return rp.generate_basic_response(content_value=cars_json)


@app.route("/cars/<id>", methods=["get"])
@jwt_required()
def get_car_by_id_order_by_price(id):
    cars_json = CarsService.filter_car_by_id(id)
    return rp.generate_basic_response(content_value=cars_json.to_json())


@app.route("/cars", methods=["POST"])
@csrf.exempt
@jwt_required()
def register_car():

    if "photo" not in request.files:
        return rp.generate_default_400_response(message="Missing picture!")

    body = {
        "title": request.form.get("title", None),
        "description": request.form.get("description", None),
        "photo": request.files["photo"],
        "year": request.form.get("year", None),
        "km": request.form.get("km", None),
        "city": request.form.get("city", None),
        "price": request.form.get("price", None),
        "category_id": request.form.get("category_id", None),
    }

    created, car = CarsService.create_car(**body)

    if created:
        return rp.generate_basic_response(car, status=201, message="Criado com sucesso")

    return rp.generate_default_400_response()


@csrf.exempt
@jwt_required()
@app.route("/cars/<id>", methods=["PUT"])
def update_car(id):

    photo = "" if "photo" not in request.files else request.files["photo"]

    body = {
        "title": request.form.get("title", None),
        "description": request.form.get("description", None),
        "photo": photo,
        "year": request.form.get("year", None),
        "km": request.form.get("km", None),
        "city": request.form.get("city", None),
        "price": request.form.get("price", None),
        "category_id": request.form.get("category_id", None),
    }

    created, car = CarsService.update_car_instance_by_id(id, **body)
    if created:
        return rp.generate_basic_response(content_value=car)
    return rp.generate_default_400_response(message=car["error"])


@csrf.exempt
@jwt_required()
@app.route("/cars/<id>", methods=["DELETE"])
def delete_car(id):
    cars_json = CarsService.delete_cat_instance_by_id(id)
    return rp.generate_basic_response(content_value=cars_json)

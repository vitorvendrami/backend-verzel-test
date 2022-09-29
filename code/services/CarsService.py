from uuid import uuid4

from app import db, app
from managers.FileManager import FileManager

from models.CarsModel import Cars
from validators.Validators import CarsValidator

bucket_name = app.config["S3_BUCKET"]


class CarsService:
    @staticmethod
    def filter_car_by_title(title):
        """Returns a car instance given it title"""
        return Cars.query.filter_by(title=title).first()

    @staticmethod
    def filter_car_by_id(id):
        """Returns a car instance given it id"""
        return Cars.query.filter_by(id=id).first()

    @staticmethod
    def return_all_cars_at_json():
        """Retriev all cars from the database"""
        cars_objects = Cars.query.all()
        json_of_cars = [car.to_json() for car in cars_objects]

        return json_of_cars

    @staticmethod
    def return_all_cars_ordered_by_price():
        """Retriev all cars from the database ordered by price"""
        cars_objects = Cars.query.order_by(Cars.price).all()
        json_of_cars = [car.to_json() for car in cars_objects]
        return json_of_cars

    @staticmethod
    def create_car(
        title: str,
        description: str,
        photo: dict,
        year: int,
        km: int,
        city: str,
        price: int,
        category_id: int,
    ):
        """Creates a car instance"""

        try:

            # make name validation
            CarsValidator(title).validate_unique_keys()

            extension = photo.filename[::-1].split('.')[0][::-1]
            file_name = FileManager.generate_new_protected_file_name(f".{extension}")

            # creates the instance of the car
            car = Cars(
                title=title,
                description=description,
                photo="{}{}".format(app.config["S3_LOCATION"], file_name),
                year=int(year),
                km=int(km),
                city=str(city),
                price=int(price),
                category_id=int(category_id),
            )
            db.session.add(car)

        except Exception as e:
            return False, {"error", e}

        else:
            # upload files to s3
            upload, file_url = FileManager.upload_file_to_s3(
                photo, file_name, bucket_name
            )

            # save
            if upload:
                db.session.commit()
                return True, car.to_json()

            return False, file_url

    @staticmethod
    def update_car_instance_by_id(
        id: int,
        title: str,
        description: str,
        photo: dict,
        year: int,
        km: int,
        city: str,
        price: int,
        category_id: int,
    ):
        """Updates a car instance given its id"""

        # get the current instance
        car_obj = CarsService.filter_car_by_id(id)

        if not car_obj:
            return {}

        try:
            if title:
                car_obj.title = title

            if description:
                car_obj.description = description

            if year:
                car_obj.year = int(year)

            if km:
                car_obj.km = int(km)

            if city:
                car_obj.city = city

            if price:
                car_obj.price = int(price)

            if category_id:
                car_obj.category_id = int(category_id)

            if photo != "":
                extension = photo.filename[::-1].split('.')[0][::-1]
                new_file_name = FileManager.generate_new_protected_file_name(f".{extension}")

                old_file_name = car_obj.photo.split(".com/")[1]
                renewed, file_url = FileManager.renew_file_from_s3(
                    photo, old_file_name=old_file_name, new_file_name=new_file_name
                )

                car_obj.picture_s3_url = file_url

            db.session.add(car_obj)
            db.session.commit()

            return True, car_obj.to_json()

        except Exception as e:
            return False, {"error", e}

    @staticmethod
    def delete_cat_instance_by_id(id):
        """Delete an instance of a car, given its id"""

        car_obj = Cars.query.filter_by(id=id).first()

        try:
            db.session.delete(car_obj)
            db.session.commit()
            return {"message": "success deleting obj"}

        except Exception as e:
            print("Erro", e)
            return {"error", e}

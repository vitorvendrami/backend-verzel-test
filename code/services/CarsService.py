from uuid import uuid4

from app import db, app
from managers.FileManager import FileManager

from models.CarsModel import Cars
from app import S3_BUCKET
from validators.Validators import CarsValidator

bucket_name = S3_BUCKET


class CarsService:

    @staticmethod
    def filter_car_by_name(name):
        """Returns a car instance given it name"""
        return Cars.query.filter_by(name=name).first()

    @staticmethod
    def filter_car_by_id(id):
        """Returns a car instance given it id"""
        return Cars.query.filter_by(id=id).first()

    @staticmethod
    def return_all_cars():
        """Retriev all cars from the database"""
        cars_objects = Cars.query.all()
        json_of_cars = [car.to_json() for car in cars_objects]

        return json_of_cars

    @staticmethod
    def create_car(name: str, brand: str, model: str, file: dict):
        """Creates a car instance"""

        # create a name for the file
        file_name = uuid4().__str__()

        try:
            # make name validation
            CarsValidator(name, model, brand).validate_unique_keys()

            extension = file.filename[-4:]
            file_name = file_name + extension

            # creates the instance of the car
            car = Cars(
                name=name,
                brand=brand,
                model=model,
                picture_s3_url="{}{}".format(app.config["S3_LOCATION"], file_name)
            )
            db.session.add(car)

        except Exception as e:
            return False, {}

        else:
            # upload files to s3
            upload, file_url = FileManager.upload_file_to_s3(
                file,
                file_name,
                bucket_name
            )

            # save
            if upload:
                db.session.commit()
                return True, car.to_json()

            return False, None

    @staticmethod
    def update_car_instance_by_id(id: int, name: str, brand: str, model: str, file: dict):
        """Updates a car instance given its id"""

        extension = file.filename[-4:]
        new_file_name = FileManager.generate_new_protected_file_name(extension)

        # get the current instance
        car_obj = CarsService.filter_car_by_id(id)

        if not car_obj:
            return {}

        try:
            if name:
                car_obj.name = name

            if brand:
                car_obj.brand = brand

            if model:
                car_obj.model = model

            if file:
                old_file_name = car_obj.picture_s3_url.split(".com/")[1]
                renewed, file_url = FileManager.renew_file_from_s3(
                    file,
                    old_file_name=old_file_name,
                    new_file_name=new_file_name
                )

            car_obj.picture_s3_url = file_url

            db.session.add(car_obj)
            db.session.commit()

            return True, car_obj.to_json()

        except Exception as e:
            return False, {}

    @staticmethod
    def delete_cat_instance_by_id(id):
        """Delete an instance of a car, given its id"""

        car_obj = Cars.query.filter_by(id=id).first()

        try:
            db.session.delete(car_obj)
            db.session.commit()
            return {"message": "success deleting obj"}

        except Exception as e:
            print('Erro', e)
            return {}

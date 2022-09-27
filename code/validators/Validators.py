from models.CarsModel import Cars
from services import CarsService


class CarsValidator(Cars):

    def __init__(self, name: str, model: str, brand: str):
        self.name = name
        self.model = model
        self.brand = brand

    def validate_unique_keys(self):
        cars = CarsService.CarsService.filter_car_by_name(self.name)
        if cars:
            raise ValueError("A car with that name already exists")

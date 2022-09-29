from models.CarsModel import Cars
from services import CarsService


class CarsValidator(Cars):
    """Class to handle Cars Model validation"""

    def __init__(self, title: str):
        self.name = title

    def validate_unique_keys(self):
        """Validates the constraint of unique fields of cars model"""
        cars = CarsService.CarsService.filter_car_by_title(self.title)
        if cars:
            raise ValueError("A car with that name already exists")

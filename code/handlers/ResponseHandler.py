import json

from flask import Response

from enums.ResponseEnum import ResponseEnum


class ResponseHandler:

    @staticmethod
    def generate_404_base_response():
        """Generate the 404 default response for the API"""
        body = {"error": ResponseEnum.BASE_NOT_FOUND_404.value}
        return Response(json.dumps(body), status=404, mimetype="application/json")

    @staticmethod
    def generate_basic_response(content_value, status=200, content_name=False, message=False):
        """Generates Basic Response"""
        body = content_value
        if content_value == {}:
            return ResponseHandler.generate_404_base_response()

        elif content_name:
            body = {content_name: content_value}
        if message:
            body["message"] = message

        return Response(json.dumps(body), status=status, mimetype="application/json")

    @staticmethod
    def generate_default_400_response():
        """Generate 400 default Response for the API"""
        body = {"error": ResponseEnum.BASE_NOT_FOUND_400.value}
        return Response(json.dumps(body), status=400, mimetype="application/json")

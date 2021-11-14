from flask import request, make_response, render_template
from flask_restful import Resource
from src.apps.Users import Users
from src.apps.Courses import Courses


def getExtraData():
    body = request.json
    headers = dict(request.headers)
    if 'Host' in headers:
        headers.pop('Host')  # Invalid header
    queryParams = request.query_string
    return body, headers, queryParams


CLASS_MAP = {
    "users": Users(),
    "courses": Courses()
}


def getCorrectEndpoint(url: str):
    values = url.split("/")
    return CLASS_MAP.get(values[0]) if len(values) else None


class Gateway(Resource):
    def get(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            return make_response({"message": "not found"}, 404)
        return resource.get(url, *getExtraData())

    def post(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            return make_response({"message": "not found"}, 404)
        return resource.post(url, *getExtraData())

    def patch(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            return make_response({"message": "not found"}, 404)
        return resource.patch(url, *getExtraData())

    def delete(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            return make_response({"message": "not found"}, 404)
        return resource.delete(url, *getExtraData())

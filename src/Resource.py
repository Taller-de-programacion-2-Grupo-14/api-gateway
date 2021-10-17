from flask import request
from flask_restful import Resource, reqparse


def parseUrl():
    body = request.json
    headers = request.headers
    print(body, headers)


class Gateway(Resource):
    def get(self, url):
        print(url)
        parseUrl()

    def post(self, url):
        parseUrl()

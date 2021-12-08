import http.client
import os

import jwt
import requests
from flask import Flask, render_template, request
from flask_restful import Api
from requests import HTTPError
from werkzeug.routing import BaseConverter
from src.Resource import Gateway

TOKEN_FIELD_NAME = "x-access-token"

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


@app.after_request
def _build_cors_post_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/doc")
def getDoc():
    return render_template("index.html")


def _getToken(headers: dict):
    keyName = None
    for key in headers.keys():
        if key.lower() == TOKEN_FIELD_NAME:
            keyName = key
    if not keyName:
        return None
    return headers.get(keyName)


def processHeader(headers, body: dict) -> (dict, bool):
    if 'Host' in headers:
        headers.pop('Host')  # Invalid header
    token = _getToken(headers)
    if not token and not (body and "user_id" in body):  # Check to not allow to bypass the token
        return body, False
    try:
        jwt.decode(token, key=os.getenv("HASH_SECRET"), algorithms=[os.getenv("HASH_ALGORITHM"), ])
        response = requests.get(f'{os.getenv("USERS_HOST")}users', headers=headers)
        response.raise_for_status()
        user = response.json()
        if user.get("blocked", False):
            return {"message": "user is blocked", "status": http.client.FORBIDDEN}, True
    except HTTPError:
        return {}, False
    except jwt.ExpiredSignatureError:
        return {"message": "expired token", "status": http.client.UNAUTHORIZED}, True
    except jwt.InvalidTokenError:
        return {"message": "invalid token", "status": http.client.FORBIDDEN}, True
    return {}, False


@app.before_request
def preRequest():
    headers = dict(request.headers)
    body, error = processHeader(headers, {})
    if error:
        return body


app.url_map.converters['regex'] = RegexConverter
api = Api(app)
api.add_resource(Gateway, '/<regex(".*"):url>')

import http.client
import os

import requests
from flask import make_response
import jwt

TOKEN_FIELD_NAME = "x-access-token"


def getQueryParams(queryParam) -> str:
    if not queryParam:
        return ""
    return f"?{str(queryParam, 'utf-8')}"


def _getToken(headers: dict):
    keyName = None
    for key in headers.keys():
        if key.lower() == TOKEN_FIELD_NAME:
            keyName = key
    if not keyName:
        return None
    return headers.get(keyName)


def processHeader(headers, body: dict) -> (dict, bool):
    token = _getToken(headers)
    if not token and not (body and "user_id" in body):  # Check to not allow to bypass the token
        return body, False
    newBody = body.copy() if body else {}
    try:
        processToken = jwt.decode(token, key=os.getenv("HASH_SECRET"), algorithms=[os.getenv("HASH_ALGORITHM"), ])
        newBody.update(processToken)
        newBody["user_id"] = processToken.get("id", "")
        newBody["email"] = processToken.get("email")
    except jwt.ExpiredSignatureError:
        return {"message": "expired token", "status": http.client.UNAUTHORIZED}, True
    except jwt.InvalidTokenError:
        return {"message": "invalid token", "status": http.client.FORBIDDEN}, True
    return newBody, False


class Courses:
    def __init__(self):
        self.host = os.getenv("COURSES_HOST")

    def get(self, url, body, headers, queryParam):
        url = f"{self.host}{url}{getQueryParams(queryParam)}"
        body, shouldFinish = processHeader(headers, body)
        if shouldFinish:
            return make_response(body, body['status'])
        response = requests.get(url, json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

    def getResponseJson(self, response):
        if response.status_code == 503 or not response.text:
            return {"message": "courses service is currently unavailable, please try later",
                    "status": http.client.SERVICE_UNAVAILABLE,
                    "error": f"{response.text}"}
        return response.json()

    def post(self, url, body, headers, queryParam):
        body, shouldFinish = processHeader(headers, body)
        if shouldFinish:
            return make_response(body, body['status'])
        response = requests.post(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

    def delete(self, url, body, headers, queryParam):
        body, shouldFinish = processHeader(headers, body)
        if shouldFinish:
            return make_response(body, body['status'])
        response = requests.delete(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

    def patch(self, url, body, headers, queryParam):
        body, shouldFinish = processHeader(headers, body)
        if shouldFinish:
            return make_response(body, body['status'])
        response = requests.patch(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

import os

import requests
from flask import make_response


def getQueryParams(queryParam) -> str:
    if not queryParam:
        return ""
    return f"?{str(queryParam, 'utf-8')}"


class Users:
    def __init__(self):
        self.host = os.getenv("USERS_HOST")

    def get(self, url, body, headers, queryParam):
        url = f"{self.host}{url}{getQueryParams(queryParam)}"
        response = requests.get(url, json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

    def getResponseJson(self, response):
        if response.status_code == 503 or not response.text:
            return {"message": "users service is currently unavailable, please try later", "status": 503}
        return response.json()

    def post(self, url, body, headers, queryParam):
        response = requests.post(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

    def delete(self, url, body, headers, queryParam):
        response = requests.delete(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

    def patch(self, url, body, headers, queryParam):
        response = requests.patch(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(self.getResponseJson(response), response.status_code)

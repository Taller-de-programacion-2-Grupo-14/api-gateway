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
        print(f"url is {url}")
        try:
            response = requests.get(url, json=body, headers=headers)
        except Exception as e:
            message = {"url": url, "error": f"{e}"}
            return make_response(message, 500)
        print(f"response is: {response} and json {response.json()}")
        return make_response(response.json(), response.status_code)

    def post(self, url, body, headers, queryParam):
        response = requests.post(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(response.json(), response.status_code)

    def delete(self, url, body, headers, queryParam):
        response = requests.delete(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(response.json(), response.status_code)

    def patch(self, url, body, headers, queryParam):
        response = requests.patch(f"{self.host}{url}{getQueryParams(queryParam)}", json=body, headers=headers)
        return make_response(response.json(), response.status_code)

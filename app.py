from flask import Flask, render_template
from flask_restful import Api
from werkzeug.routing import BaseConverter

from src.Resource import Gateway

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


app.url_map.converters['regex'] = RegexConverter
api = Api(app)
api.add_resource(Gateway, '/<regex(".*"):url>')

from werkzeug.routing import BaseConverter
from flask import Flask
from flask_restful import Api
from src.Resource import Gateway

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter
api = Api(app)
api.add_resource(Gateway, '/<regex(".*"):url>')
from flask import Flask
from flask_restful import Api, Resource
from util import data_file_abs
import json

app = Flask(__name__)
api = Api(app)


class NewContributors(Resource):
    def get(self):
        data = []
        with open(data_file_abs()) as f:
            for line in f:
                data.append(json.loads(line))

        return data


api.add_resource(NewContributors, '/new_contributors')


def start_api(): app.run(port='5002')

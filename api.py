from Time_Matters_SingleDoc import Time_Matters_SingleDoc, Time_Matters_SingleDoc_PerSentence
from flask import Flask, request
from flask_restplus import Api, Resource, fields, inputs
from flask import Flask
from flask_cors import CORS, cross_origin
from query import time_matters_query
flask_app = Flask(__name__)
app = Api(app=flask_app)
name_space = app.namespace('Time-Matters-query', description='get relevant dates and his score form a arquivo.pt query')
CORS(flask_app)

@name_space.route("/")
class MyResource(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'query': 'Insert query'})
    def get(self):
        query_text = str(request.args.get('query'))
        json_dates = time_matters_query(query_text, 2)
        return json_dates


if __name__ == '__main__':
    flask_app.debug = True
    flask_app.run()

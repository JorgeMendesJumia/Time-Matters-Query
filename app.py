from flask import request
from flask_restplus import Api, Resource
from flask import Flask
from flask_cors import CORS
from query import time_matters_query
import os

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
    port = int(os.environ.get("PORT", 443))
    flask_app.run(host='0.0.0.0', port=port)
    flask_app.run()

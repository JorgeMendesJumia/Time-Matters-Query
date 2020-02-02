from flask import Flask, request
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_cors import CORS
from query_dev import Time_Matters_Query


def main():
    """The main function for this script."""
    app.run(host='127.0.0.1', port=443, debug=True)
    CORS(app)


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.config['SWAGGER'] = {
  "title": "Time-Matters-API",
  "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "false"),
  ],
  "info": {
    "title": "Time-Matters",
    "description": "Date extractor that scores the relevance of temporal expressions found within a text (single document) or a set of texts (multiple documents).",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "schemes": [
    "https",
    "http"
  ]
}

Swagger(app)
@app.route('/Query/api/v1.0/arquivo.pt', methods=['GET'])
@swag_from('query.yml')
def single_doc_bySentence():
    query_text = str(request.args.get('query_text'))
    num_of_docs = str(request.args.get('num_of_docs'))
    offset = str(request.args.get('offset'))
    search_type = str(request.args.get('search_type'))
    date_extractor = str(request.args.get('date_extractor'))

    json_dates = Time_Matters_Query(query_text, num_of_docs, offset, search_type, date_extractor)
    return json_dates


def heroku_set_permissions(heroku=True):
    import imp
    import os
    if heroku:
        path = imp.find_module('py_heideltime')[1]
        full_path = path + "/Heideltime/TreeTaggerLinux/bin/*"
        command = 'chmod 111 ' + full_path
        os.popen(command).read()


if __name__== '__main__':

  main()
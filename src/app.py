import json
import logging
from logging.config import dictConfig
from flask import Flask, request, Response
from flask_restful import Resource, Api

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s.%(funcName)s:%(lineno)s: %(message)s',
    }},
    'handlers': {'stdout': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['stdout']
    }
})

app = Flask(__name__)
api = Api(app)
app.logger.setLevel(logging.INFO)


class health(Resource):

    @staticmethod
    def get():
        logger = logging.getLogger(__name__)
        logger.info("Health Get")

        return Response(json.dumps("Get successful"), status=200, mimetype='application/json')

    @staticmethod
    def post():
        logger = logging.getLogger(__name__)
        logger.info("Health Post")

        req = request.get_json()

        logger.info(req)

        my_field = req.get('test_field', '')

        logger.info('Got field {0}'.format(my_field))

        return Response(json.dumps('Post successful'), status=200, mimetype='application/json')


api.add_resource(health, '/health')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
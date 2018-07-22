import json
import logging
from logging.config import dictConfig
from flask import Flask, request, Response
from flask_restful import Resource, Api
import interview

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


class interview_request(Resource):

    @staticmethod
    def get():
        logger = logging.getLogger(__name__)
        logger.info("Interview Post")

        req = request.get_json()

        logger.info(req)

        tag = req.get('tag', 'default')
        user_id = req.get('user_id', '0000000000')
        level_id = req.get('level_id', '0')

        message = interview.get_random_response_by_tag_level(user_id, tag, level_id)

        return Response(json.dumps({'message': message}), status=200, mimetype='application/json')

    @staticmethod
    def post():
        logger = logging.getLogger(__name__)
        logger.info("Interview Post")

        req = request.get_json()

        logger.info(req)

        tag = req.get('tag', 'default')
        user_resp = req.get('user_resp', '')
        level_id = req.get('level_id', '0')
        user_id = req.get('user_id', '0000000000')

        accepted = interview.validate_and_insert(tag, level_id, user_resp, user_id)



        if accepted:
            return Response(json.dumps('Post successful'), status=202, mimetype='application/json')
        else:
            return Response(json.dumps('Post rejected'), status=406, mimetype='application/json')


class health(Resource):

    @staticmethod
    def get():
        logger = logging.getLogger(__name__)
        logger.info("Health GET started.")

        return Response(json.dumps("Healthy"), status=200, mimetype='application/json')


api.add_resource(health, '/health')
api.add_resource(interview_request, '/interview')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

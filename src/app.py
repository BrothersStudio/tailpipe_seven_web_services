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

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
                    )

class InterviewRequest(Resource):

    @staticmethod
    def get():
        logging.info("Interview GET")

        args = request.args

        logging.info(args)

        tag = args['tag'] if 'tag' in args else 'default'
        user_id = str(args['user_id']) if 'user_id' in args else '0000000000'
        level = str(args['level']) if 'level' in args else '0'

        message = interview.get_random_response_by_tag_level(user_id, tag, level)

        response = {'message': message, 'user_id': user_id, 'tag': tag, 'level': level}

        return Response(json.dumps(response), status=200, mimetype='application/json')

    @staticmethod
    def post():
        logging.info("Interview POST")

        req = request.get_json()

        logging.info(req)

        tag = req.get('tag', 'default')
        user_resp = req.get('message', '')
        level_id = req.get('level', '0')
        user_id = req.get('user_id', '0000000000')

        accepted = interview.validate_and_insert(tag, level_id, user_resp, user_id)

        if accepted:
            return Response(json.dumps('Post successful'), status=202, mimetype='application/json')
        else:
            return Response(json.dumps('Post rejected'), status=406, mimetype='application/json')


class Health(Resource):

    @staticmethod
    def get():
        logging.info("Health GET started.")

        return Response(json.dumps("Healthy"), status=200, mimetype='application/json')


api.add_resource(Health, '/health')
api.add_resource(InterviewRequest, '/interview')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

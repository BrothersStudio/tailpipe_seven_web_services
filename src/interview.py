import dynamo_uitls
import os
import logging
import mysql_utils

db = mysql_utils.mysqlInterview()

def validate_and_insert(tag, level, user_msg, user_id):
    logger = logging.getLogger(__name__)

    if validate_user_input(user_msg):
        db.insert_interview(level, tag, user_id, user_msg)
    else:
        return False

    logger.info('Insert into {0} successful'.format(os.environ['MYSQL_DB']))
    return True


def validate_user_input(message):
    return True


def get_random_response_by_tag_level(user_id, tag, level):
    logger = logging.getLogger(__name__)

    response = db.select_interview(tag, level, user_id)

    logger.info('Got response {0}'.format(response))

    return response

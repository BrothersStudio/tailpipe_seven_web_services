import os
import logging
import mysql_utils

db = mysql_utils.mysqlInterview()


def validate_and_insert(tag, level, user_msg, user_id):
    if validate_user_input(user_id, user_msg):
        db.insert_interview(level, tag, user_id, user_msg)
    else:
        logging.info('Message has failed validation and been rejected')
        return False

    logging.info('Insert into {0} successful'.format(os.environ['MYSQL_DB']))
    return True


def validate_user_input(user_id, message):
    if len(user_id) != 10:
        return False

    if len(message) > 612:
        return False

    for char in message:
        if any(x in char for x in ['+', '#', '$', '@', '%', '^', '(', ')', '[', ']', '{', '}', '<', '>', '|']):
            return False

    return True


def get_random_response_by_tag_level(user_id, tag, level):
    response = db.select_interview(tag, level, user_id)

    logging.info('Got response {0}'.format(response))

    return response

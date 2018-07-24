import boto3
import logging


def get_conn():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    return dynamodb


def insert(input_dict, table_name):
    try:
        table = get_conn().Table(table_name)

        table.put_item(Item=input_dict)

    except Exception as e:
        logging.warning('Got Exception {0}'.format(e))
        return False

    return True


def get(key_dict, table_name):
    try:
        table = get_conn().Table(table_name)

        response = table.get_item(Key=key_dict)

    except Exception as e:
        logging.warning('Got Exception {0}'.format(e))
        return {}

    return response

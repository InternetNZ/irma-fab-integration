"""
A module to implement FAB related requirements
"""
import os

import boto3

from fab import logger

DYNAMODB_ENDPOINT_URL = os.environ.get('DYNAMODB_ENDPOINT_URL')
DYNAMODB_TABLE_NAME = 'fab-vc'


def save_fab_vc(verifiable_credential):
    """
    This receives a verifiable credential as a string and stores it in a DynamoDB table

    :param verifiable_credential: Verifiable Credential string
    """
    logger.info("Writing FAB VC to DynamoDB: %s...", DYNAMODB_ENDPOINT_URL)
    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)

    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(
        Item={
            'id': verifiable_credential.get('proof')['challenge'],
            'vc': verifiable_credential,
        }
    )


def get_fab_vc(vc_id):
    """
    Fetches a stored FAB verifiable credential by given (session) id.

    :param vc_id: challenge ID in FAB context
    :return: VC
    """
    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    response = table.get_item(Key={
        'id': vc_id
    })

    item = response.get('Item')
    if item:
        return item['vc']

    return None

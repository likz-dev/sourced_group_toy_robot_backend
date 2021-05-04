from decimal import Decimal

import boto3
from moto import mock_dynamodb2
from moto.secretsmanager import mock_secretsmanager

from app.daos.toy_robot_session import ToyRobotSession


def initialize_secrets():
    conn = boto3.client('secretsmanager')

    conn.create_secret(
        Name='DatabaseCredentials', SecretString='{"db_name": "test_ddb_name"}'
    )


def initialize_dynamodb():
    name = 'test_ddb_name'
    conn = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id='ak',
        aws_secret_access_key='sk',
    )
    conn.create_table(
        TableName=name,
        KeySchema=[{'AttributeName': 'session_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'session_id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
    )


@mock_secretsmanager
@mock_dynamodb2
def test_item_add_empty_string_attr_no_exception():
    initialize_secrets()
    initialize_dynamodb()

    toy_robot_session = ToyRobotSession()
    toy_robot_session.put_session('11111111-2222-3333-4444-555555555555', {'y': 0, 'facing': 'NORTH', 'x': 0})
    assert toy_robot_session.get_session('11111111-2222-3333-4444-555555555555') == {'facing': 'NORTH',
                                                                                     'session_id': '11111111-2222-3333-4444-555555555555',
                                                                                     'x': Decimal('0'),
                                                                                     'y': Decimal('0')}

    toy_robot_session.update_session('11111111-2222-3333-4444-555555555555', {'y': 1, 'facing': 'SOUTH', 'x': 1})
    assert toy_robot_session.get_session('11111111-2222-3333-4444-555555555555') == {'facing': 'SOUTH',
                                                                                     'session_id': '11111111-2222-3333-4444-555555555555',
                                                                                     'x': Decimal('1'),
                                                                                     'y': Decimal('1')}

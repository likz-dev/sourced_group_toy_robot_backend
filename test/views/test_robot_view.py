import uuid
from decimal import Decimal

import boto3
from mock import MagicMock
from moto.secretsmanager import mock_secretsmanager

from app.exceptions.robot_exception import ERROR_ROBOT_MISSING_PARAMS, ERROR_ROBOT_NOT_INITIALIZED, \
    ERROR_ROBOT_OFF_THE_BOARD
from app.daos.toy_robot_session import ToyRobotSession


def initialize_secrets():
    conn = boto3.client("secretsmanager")

    conn.create_secret(
        Name="DatabaseCredentials", SecretString='{"db_name": "test_ddb_name"}'
    )


@mock_secretsmanager
def test_place_new_session(app, client):
    initialize_secrets()

    ToyRobotSession.put_session = MagicMock()
    uuid.uuid4 = MagicMock(return_value='11111111-2222-3333-4444-555555555555')

    res = client.get('/place?x=1&y=2&facing=NORTH')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': '1', 'y': '2', 'facing': 'NORTH', 'session_id': '11111111-2222-3333-4444-555555555555'}

@mock_secretsmanager
def test_place_existing_session(app, client):
    initialize_secrets()

    ToyRobotSession.get_session = MagicMock(
        return_value={'y': Decimal('0'), 'facing': 'NORTH', 'x': Decimal('0'),
                      'session_id': '11111111-2222-3333-4444-555555555555'})
    ToyRobotSession.update_session = MagicMock()

    res = client.get('/place?x=2&y=2&facing=NORTH&session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': '2', 'y': '2', 'facing': 'NORTH'}


@mock_secretsmanager
def test_place_new_session_invalid(app, client):
    initialize_secrets()

    uuid.uuid4 = MagicMock(return_value='11111111-2222-3333-4444-555555555555')

    res = client.get('/place')
    error_message = str(res.data)

    assert res.status_code == 500
    assert ERROR_ROBOT_MISSING_PARAMS in error_message


@mock_secretsmanager
def test_move_robot(app, client):
    initialize_secrets()

    ToyRobotSession.get_session = MagicMock(
        return_value={'y': Decimal('4'), 'facing': 'SOUTH', 'x': Decimal('3'),
                      'session_id': '11111111-2222-3333-4444-555555555555'})
    ToyRobotSession.update_session = MagicMock()

    res = client.get('/move?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 3, 'facing': 'SOUTH'}


@mock_secretsmanager
def test_move_robot_uninitialised(app, client):
    initialize_secrets()

    res = client.get('/move')

    error_message = str(res.data)

    assert res.status_code == 500
    assert ERROR_ROBOT_NOT_INITIALIZED in error_message


@mock_secretsmanager
def test_move_robot_off_the_board(app, client):
    initialize_secrets()

    ToyRobotSession.get_session = MagicMock(
        return_value={'y': Decimal('4'), 'facing': 'NORTH', 'x': Decimal('3'),
                      'session_id': '11111111-2222-3333-4444-555555555555'})
    ToyRobotSession.update_session = MagicMock()

    res = client.get('/move?session_id=11111111-2222-3333-4444-555555555555')
    error_message = str(res.data)

    assert res.status_code == 500
    assert ERROR_ROBOT_OFF_THE_BOARD in error_message


@mock_secretsmanager
def test_rotate_left(app, client):
    initialize_secrets()

    ToyRobotSession.get_session = MagicMock(
        return_value={'y': Decimal('4'), 'facing': 'SOUTH', 'x': Decimal('3'),
                      'session_id': '11111111-2222-3333-4444-555555555555'})
    ToyRobotSession.update_session = MagicMock()

    res = client.get('/left?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 4, 'facing': 'EAST'}


@mock_secretsmanager
def test_rotate_right(app, client):
    initialize_secrets()

    ToyRobotSession.get_session = MagicMock(
        return_value={'y': Decimal('4'), 'facing': 'SOUTH', 'x': Decimal('3'),
                      'session_id': '11111111-2222-3333-4444-555555555555'})
    ToyRobotSession.update_session = MagicMock()

    res = client.get('/right?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 4, 'facing': 'WEST'}


@mock_secretsmanager
def test_report(app, client):
    initialize_secrets()

    ToyRobotSession.get_session = MagicMock(
        return_value={'y': Decimal('4'), 'facing': 'SOUTH', 'x': Decimal('3'),
                      'session_id': '11111111-2222-3333-4444-555555555555'})

    res = client.get('/report?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 4, 'facing': 'SOUTH'}

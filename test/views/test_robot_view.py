import uuid

from mock import MagicMock

from exceptions.robot_exception import ERROR_ROBOT_MISSING_PARAMS, ERROR_ROBOT_NOT_INITIALIZED, \
    ERROR_ROBOT_OFF_THE_BOARD


def test_place_new_session(app, client):
    uuid.uuid4 = MagicMock(return_value='11111111-2222-3333-4444-555555555555')

    res = client.get('/place?x=1&y=2&facing=NORTH')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': '1', 'y': '2', 'facing': 'NORTH', 'session_id': '11111111-2222-3333-4444-555555555555'}


def test_place_existing_session(app, client):
    with client as c:
        with c.session_transaction() as sess:
            sess['11111111-2222-3333-4444-555555555555'] = {
                'robot': {'x': '3', 'y': '4', 'facing': 'SOUTH'}
            }

        res = c.get('/place?x=2&y=2&facing=NORTH&session_id=11111111-2222-3333-4444-555555555555')
        body = res.get_json()

        assert res.status_code == 200
        assert body == {'x': '2', 'y': '2', 'facing': 'NORTH'}


def test_place_new_session_invalid(app, client):
    uuid.uuid4 = MagicMock(return_value='11111111-2222-3333-4444-555555555555')

    res = client.get('/place')
    error_message = str(res.data)

    assert res.status_code == 500
    assert ERROR_ROBOT_MISSING_PARAMS in error_message


def test_move_robot(app, client):
    with client as c:
        with c.session_transaction() as sess:
            sess['11111111-2222-3333-4444-555555555555'] = {
                'robot': {'x': '3', 'y': '4', 'facing': 'SOUTH'}
            }

    res = client.get('/move?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 3, 'facing': 'SOUTH'}


def test_move_robot_uninitialised(app, client):
    res = client.get('/move')

    error_message = str(res.data)

    assert res.status_code == 500
    assert ERROR_ROBOT_NOT_INITIALIZED in error_message


def test_move_robot_off_the_board(app, client):
    with client as c:
        with c.session_transaction() as sess:
            sess['11111111-2222-3333-4444-555555555555'] = {
                'robot': {'x': '3', 'y': '4', 'facing': 'NORTH'}
            }

    res = client.get('/move?session_id=11111111-2222-3333-4444-555555555555')
    error_message = str(res.data)

    assert res.status_code == 500
    assert ERROR_ROBOT_OFF_THE_BOARD in error_message


def test_rotate_left(app, client):
    with client as c:
        with c.session_transaction() as sess:
            sess['11111111-2222-3333-4444-555555555555'] = {
                'robot': {'x': '3', 'y': '4', 'facing': 'SOUTH'}
            }

    res = client.get('/left?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 4, 'facing': 'EAST'}


def test_rotate_right(app, client):
    with client as c:
        with c.session_transaction() as sess:
            sess['11111111-2222-3333-4444-555555555555'] = {
                'robot': {'x': '3', 'y': '4', 'facing': 'SOUTH'}
            }

    res = client.get('/right?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 4, 'facing': 'WEST'}


def test_report(app, client):
    with client as c:
        with c.session_transaction() as sess:
            sess['11111111-2222-3333-4444-555555555555'] = {
                'robot': {'x': '3', 'y': '4', 'facing': 'SOUTH'}
            }

    res = client.get('/report?session_id=11111111-2222-3333-4444-555555555555')
    body = res.get_json()

    assert res.status_code == 200
    assert body == {'x': 3, 'y': 4, 'facing': 'SOUTH'}

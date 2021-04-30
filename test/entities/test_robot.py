import pytest

from entities.robot import Robot, DIRECTION_NORTH, DIRECTION_WEST, DIRECTION_SOUTH, DIRECTION_EAST
from exceptions.robot_exception import RobotException, ERROR_ROBOT_NOT_INITIALIZED, ERROR_ROBOT_OFF_THE_BOARD, \
    ERROR_ROBOT_MISSING_PARAMS


@pytest.fixture
def mock_robot():
    robot = Robot()
    return robot


def test_robot_uninitialized(mock_robot):
    with pytest.raises(RobotException) as exception:
        mock_robot.move()

    error_message = exception.value.message
    assert error_message == ERROR_ROBOT_NOT_INITIALIZED


def test_place(mock_robot):
    mock_robot.place(1, 2, DIRECTION_NORTH)
    assert mock_robot.x == 1
    assert mock_robot.y == 2
    assert mock_robot.facing == DIRECTION_NORTH


def test_place_invalid(mock_robot):
    with pytest.raises(RobotException) as exception:
        mock_robot.place(1, 2, None)

    error_message = exception.value.message
    assert error_message == ERROR_ROBOT_MISSING_PARAMS


@pytest.mark.parametrize('current_facing, expected_facing', [
    (DIRECTION_NORTH, DIRECTION_WEST),
    (DIRECTION_WEST, DIRECTION_SOUTH),
    (DIRECTION_SOUTH, DIRECTION_EAST),
    (DIRECTION_EAST, DIRECTION_NORTH),
])
def test_left(current_facing, expected_facing, mock_robot):
    mock_robot.place(0, 0, current_facing)
    mock_robot.left()
    assert mock_robot.facing == expected_facing


@pytest.mark.parametrize('current_facing, expected_facing', [
    (DIRECTION_NORTH, DIRECTION_EAST),
    (DIRECTION_EAST, DIRECTION_SOUTH),
    (DIRECTION_SOUTH, DIRECTION_WEST),
    (DIRECTION_WEST, DIRECTION_NORTH),
])
def test_right(current_facing, expected_facing, mock_robot):
    mock_robot.place(0, 0, current_facing)
    mock_robot.right()
    assert mock_robot.facing == expected_facing


@pytest.mark.parametrize('current_facing, expected_x, expected_y', [
    (DIRECTION_NORTH, 1, 3),
    (DIRECTION_EAST, 2, 2),
    (DIRECTION_SOUTH, 1, 1),
    (DIRECTION_WEST, 0, 2),
])
def test_move_valid(current_facing, expected_x, expected_y, mock_robot):
    mock_robot.place(1, 2, current_facing)
    success = mock_robot.move()
    assert mock_robot.x == expected_x
    assert mock_robot.y == expected_y
    assert success is True


@pytest.mark.parametrize('current_x, current_y, current_facing, expected_x, expected_y', [
    (5, 5, DIRECTION_NORTH, 5, 5),
    (5, 5, DIRECTION_EAST, 5, 5),
    (0, 0, DIRECTION_SOUTH, 0, 0),
    (0, 0, DIRECTION_WEST, 0, 0),
])
def test_move_invalid(current_x, current_y, current_facing, expected_x, expected_y, mock_robot):
    mock_robot.place(current_y, current_y, current_facing)

    with pytest.raises(RobotException) as exception:
        mock_robot.move()

    assert mock_robot.x == expected_x
    assert mock_robot.y == expected_y

    error_message = exception.value.message
    assert error_message == ERROR_ROBOT_OFF_THE_BOARD


@pytest.mark.parametrize('current_x, current_y, success', [
    (4, 6, False),
    (6, 4, False),
    (4, -1, False),
    (-1, 4, False),
    (4, 4, True)
])
def test_is_valid_move(current_x, current_y, success, mock_robot):
    mock_robot.place(current_x, current_y, DIRECTION_NORTH)
    assert mock_robot.is_valid_move() == success


def test_report(mock_robot):
    mock_robot.place(1, 2, DIRECTION_NORTH)
    assert mock_robot.report() == {
        'x': 1,
        'y': 2,
        'facing': DIRECTION_NORTH
    }

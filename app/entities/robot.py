from functools import wraps

from app.exceptions.robot_exception import RobotException, ERROR_ROBOT_NOT_INITIALIZED, ERROR_ROBOT_OFF_THE_BOARD, \
    ERROR_ROBOT_MISSING_PARAMS

BOARD_SIZE_X = 5
BOARD_SIZE_Y = 5

DIRECTION_NORTH = 'NORTH'
DIRECTION_WEST = 'WEST'
DIRECTION_SOUTH = 'SOUTH'
DIRECTION_EAST = 'EAST'

KEY_X = 'x'
KEY_Y = 'y'
KEY_FACING = 'facing'


def is_placed(f):
    @wraps(f)
    def decorated(robot):
        if not robot.initialized:
            raise RobotException(ERROR_ROBOT_NOT_INITIALIZED)
        return f(robot)

    return decorated


class Robot:
    def __init__(self, args=None):
        if args:
            self.x = int(args.get(KEY_X))
            self.y = int(args.get(KEY_Y))
            self.facing = args.get(KEY_FACING)
            self.initialized = True
        else:
            self.x = None
            self.y = None
            self.facing = None
            self.initialized = False

    def place(self, x, y, facing):
        if x is None or y is None or facing is None:
            raise RobotException(ERROR_ROBOT_MISSING_PARAMS)

        self.x = x
        self.y = y
        self.facing = facing
        self.initialized = True

    @is_placed
    def move(self):
        tmp_y = self.y
        tmp_x = self.x

        if self.facing == DIRECTION_NORTH:
            self.y += 1
        if self.facing == DIRECTION_SOUTH:
            self.y -= 1
        if self.facing == DIRECTION_EAST:
            self.x += 1
        if self.facing == DIRECTION_WEST:
            self.x -= 1

        if not self.is_valid_move():
            self.x = tmp_x
            self.y = tmp_y
            raise RobotException(ERROR_ROBOT_OFF_THE_BOARD)

        return True

    @is_placed
    def left(self):
        if self.facing == DIRECTION_NORTH:
            self.facing = DIRECTION_WEST
        elif self.facing == DIRECTION_WEST:
            self.facing = DIRECTION_SOUTH
        elif self.facing == DIRECTION_SOUTH:
            self.facing = DIRECTION_EAST
        else:
            self.facing = DIRECTION_NORTH

    @is_placed
    def right(self):
        if self.facing == DIRECTION_NORTH:
            self.facing = DIRECTION_EAST
        elif self.facing == DIRECTION_EAST:
            self.facing = DIRECTION_SOUTH
        elif self.facing == DIRECTION_SOUTH:
            self.facing = DIRECTION_WEST
        else:
            self.facing = DIRECTION_NORTH

    def is_valid_move(self):
        # Move is valid as long as the robot is on the board
        return 0 <= self.x < BOARD_SIZE_X and 0 <= self.y < BOARD_SIZE_Y

    @is_placed
    def report(self):
        return {
            KEY_X: self.x,
            KEY_Y: self.y,
            KEY_FACING: self.facing
        }

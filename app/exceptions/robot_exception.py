ERROR_ROBOT_OFF_THE_BOARD = 'The robot fell off the board. It can only move within the 5x5 board.'
ERROR_ROBOT_NOT_INITIALIZED = 'Please place the robot on the board first before continuing.'
ERROR_ROBOT_UNEXPECTED_ERROR = 'An unexpected error occurred.'
ERROR_ROBOT_MISSING_PARAMS = 'Missing parameters. Please check your request.'


class RobotException(Exception):
    def __init__(self, message=ERROR_ROBOT_UNEXPECTED_ERROR):
        self.message = message
        super().__init__(self.message)

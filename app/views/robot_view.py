import uuid

from flask import session, request, abort

from app.entities import robot
from app.entities.robot import Robot
from app.exceptions.robot_exception import RobotException
from app.daos.toy_robot_session import ToyRobotSession

KEY_SESSION_ROBOT = 'robot'
KEY_SESSION_ID = 'session_id'


def generate_session_id():
    return str(uuid.uuid4())


class RobotView:
    def __init__(self):
        self.args = request.args
        self.toy_robot_session = ToyRobotSession()
        self.session_id = self.args.get(KEY_SESSION_ID)

        if self.session_id:
            # If there is an existing session, then reconstruct the robot using session info
            robot_session_info = self.toy_robot_session.get_session(self.session_id)
            self.robot = Robot(robot_session_info)
            self.robot.report()
        else:
            # If no session, create empty robot
            self.robot = Robot()

    def create_session(self, session_id):
        self.toy_robot_session.put_session(session_id, self.robot.report())

    def update_session(self):
        self.toy_robot_session.update_session(self.session_id, self.robot.report())

    def place_robot(self):
        x = self.args.get(robot.KEY_X)
        y = self.args.get(robot.KEY_Y)
        facing = self.args.get(robot.KEY_FACING)

        # If robot is initialized means there is an existing session
        existing_session = self.robot.initialized
        try:
            self.robot.place(x, y, facing)
        except RobotException as e:
            abort(500, e.message)

        if existing_session:
            self.update_session()
            return self.robot.report()
        else:
            new_session_id = generate_session_id()
            self.create_session(new_session_id)

            response = self.robot.report()
            response['session_id'] = new_session_id

            return response

    def move_robot(self):
        try:
            self.robot.move()
            self.update_session()
            return self.robot.report()
        except RobotException as e:
            abort(500, e.message)

    def rotate_left(self):
        self.robot.left()
        self.update_session()
        return self.robot.report()

    def rotate_right(self):
        self.robot.right()
        self.update_session()
        return self.robot.report()

    def report(self):
        return self.robot.report()

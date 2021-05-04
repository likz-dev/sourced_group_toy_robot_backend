import uuid

from flask import session, request, abort

from entities import robot
from entities.robot import Robot
from exceptions.robot_exception import RobotException

KEY_SESSION_ROBOT = 'robot'
KEY_SESSION_ID = 'session_id'


def generate_session_id():
    return str(uuid.uuid4())


class RobotView:
    def __init__(self):
        self.args = request.args
        session_id = self.args.get(KEY_SESSION_ID)

        if session_id:
            print(type(session_id))
            print(f'using session_id {session_id}')
            print(session.get(session_id))
            # If there is an existing session, then reconstruct the robot using session info
            robot_session_info = session.get(session_id).get(KEY_SESSION_ROBOT)
            self.robot = Robot(robot_session_info)
            self.robot.report()
        else:
            # If no session, create empty robot
            self.robot = Robot()

    def create_session(self, session_id):
        print(f'creating new session with id: {session_id}')
        session[session_id] = {
            KEY_SESSION_ROBOT: self.robot.report()
        }
        print(session)
        print(session[session_id])
        print(session.get(session_id))

    def update_session(self):
        session_id = self.args.get(KEY_SESSION_ID)
        session[session_id] = {
            KEY_SESSION_ROBOT: self.robot.report()
        }

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
            session_id = generate_session_id()
            self.create_session(session_id)

            response = self.robot.report()
            response['session_id'] = session_id

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

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from app.views.robot_view import RobotView
from app.utils.secrets_manager import SECRET_STRING_FLASK_SECRET_KEY, SecretsManager, SECRET_NAME_FLASK

secrets_manager = SecretsManager()
flask_secrets = secrets_manager.get_value(SECRET_NAME_FLASK)

# Setup Flask application
app = Flask(__name__)
app.secret_key = flask_secrets.get(SECRET_STRING_FLASK_SECRET_KEY)
app.secret_key = 'SECRET'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

SUCCESS_RESPONSE_TEMPLATE = {'success': True}
FAILURE_RESPONSE_TEMPLATE = {'success': False}


@app.route('/test')
def hello_world():
    return {'healthy': True}


# [GET] Place the robot on the board
@app.route('/place')
def place():
    robot_view = RobotView()
    response = robot_view.place_robot()

    return response


# [GET] Move the robot forward
@app.route('/move')
def move():
    robot_view = RobotView()
    response = robot_view.move_robot()
    return response


# [GET] Rotate the robot left
@app.route('/left')
def left():
    robot_view = RobotView()
    response = robot_view.rotate_left()
    return response


# [GET] Rotate the robot right
@app.route('/right')
def right():
    robot_view = RobotView()
    response = robot_view.rotate_right()
    return response


# [GET] Returns the robot's current position and facing direction
@app.route('/report')
def report():
    robot_view = RobotView()
    response = robot_view.report()
    return response


if __name__ == '__main__':
    app.run()

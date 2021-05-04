from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from app.views.robot_view import RobotView

# Setup Flask application

app = Flask(__name__)
# app.secret_key = flask_secrets.get(SECRET_STRING_FLASK_SECRET_KEY)
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


# api.add_resource(RobotView, '/place')
# [GET] Move the robot forward
# api.add_resource(RobotView, '/move')
# # [GET] Rotate the robot 90 degrees anti clockwise
# api.add_resource(RobotView, '/left')
# # [GET] Rotate the robot 90 degrees clockwise
# api.add_resource(RobotView, '/right')
# # [GET] Retrieve the robot's current position and facing direction
# api.add_resource(RobotView, '/report')

if __name__ == '__main__':
    app.run()

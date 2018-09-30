from flask import request, jsonify, Response
from settings import app
import jwt
import datetime
from functools import wraps

# For developing without RASPBERRRY PI
from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED

from models import User

GARAGE = LED(5)
GATE = LED(6)
GARAGE_STATUS = Button(13)
GATE_STATUS = Button(19)

TOKEN_TIMEOUT = 300  # Token expire in seconds

# export GPIOZERO_PIN_FACTORY=mock
Device.pin_factory = MockFactory()  # For developing without RASPBERRRY PI


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=TOKEN_TIMEOUT)
        token = jwt.encode({'exp': expiration_date},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Unauthorized user'})
    return wrapper


@app.route('/status')
@token_required
def get_status():
    if GARAGE_STATUS.is_pressed:
        return "True"
    else:
        return "False"


@app.route('/to_open')
@token_required
def to_open():
    if GARAGE_STATUS.is_pressed:
        return "True"
    else:
        return "False"


@app.route('/to_close')
@token_required
def to_close():
    if GARAGE_STATUS.is_pressed:
        return "True"
    else:
        return "False"


@app.route('/re_open')
@token_required
def re_open():
    if GARAGE_STATUS.is_pressed:
        return "True"
    else:
        return "False"


@app.route('/re_close')
@token_required
def re_close():
    if GARAGE_STATUS.is_pressed:
        return "True"
    else:
        return "False"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

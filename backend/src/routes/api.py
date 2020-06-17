"""
    Contains API endpoints interfaced by the application's front end.
    API endpoints are created via Blueprint objects, which specify URL prefixes different routes.
"""
from flask import request, jsonify, Blueprint


''' Route blueprints '''

index = Blueprint('index', __name__, url_prefix='/')
user = Blueprint('user', __name__, url_prefix='/user')


''' non-user routes '''

@index.route('/', methods=['GET', 'POST'])
def landingPage():
    return jsonify({'message': 'Hello World!'})


@index.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    return jsonify({'route_hit': 'sign-up'})


@index.route('/sign-in', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        signInData = dict(request.get_json())
        return jsonify({'signInData': signInData })
    else:
        return jsonify({'route_hit': 'sign-in'})


''' user routes '''

@user.route('/', methods=['GET', 'POST'])
def getUser():
    return jsonify({'message': 'Hello User!'})


"""
    Contains API endpoints interfaced by the application's front end.
    API endpoints are created via Blueprint objects, which specify URL prefixes different routes.
"""
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


def generateSessionToken(username):
    return create_access_token(identity={'username': username, 'id': 123})


''' Route blueprints '''

index = Blueprint('index', __name__, url_prefix='/')
user = Blueprint('user', __name__, url_prefix='/user')


''' test routes '''

@index.route('/test', methods=['GET', 'POST'])
def testRoute():
    username = request.args.get('username')
    if username is None:
        return jsonify({'error': 'no username provided'})
    token = generateSessionToken(username)
    return jsonify({'testData': 'Some test data!', 'sessionToken': token})


@index.route('/protected-test', methods=['GET', 'POST'])
@jwt_required
def protectedTestRoute():
    user = get_jwt_identity()
    return jsonify({'user': user})


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


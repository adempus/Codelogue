"""
    Contains API endpoints interfaced by the application's front end.
    API endpoints are created via Blueprint objects, which specify URL prefixes different routes.
"""
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..app import functions

''' Route blueprints '''

index = Blueprint('index', __name__, url_prefix='/')
user = Blueprint('user', __name__, url_prefix='/user')


''' test routes '''

@index.route('/test', methods=['GET', 'POST'])
def testRoute():
    username = request.args.get('username')
    if username is None:
        return jsonify({'error': 'no username provided'})
    token = functions.generateSessionToken(username)
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


@index.route('/sign-up', methods=['POST'])
def signUp():
    if request.method == 'POST':
        signUpData = dict(request.get_json())
        print(f'Sign up data: \n{signUpData}')
        resPayload = functions.signUpUser(signUpData)
        return jsonify(resPayload)


@index.route('/sign-in', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        signInData = dict(request.get_json())
        resPayload = functions.signInUser(signInData)
        print(f'sign in response payload: {resPayload}')
        return resPayload


''' user routes '''

@user.route('/', methods=['GET', 'POST'])
def getUser():
    return jsonify({'message': 'Hello User!'})


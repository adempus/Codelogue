"""
Contains app functionality for the app's features. Most of these functions are invoked via API routes.
"""
from graphql_relay.node.node import from_global_id
from flask_jwt_extended import create_access_token
from flask import make_response, jsonify
from .models import User
from .setup import db
import bcrypt


def signUpUser(user):
    if None not in user.values():
        email, username = user['email'].strip(), user['username'].strip()
        emailQuery = User.query.filter_by(email=email).first()
        usernameQuery = User.query.filter_by(username=username).first()
        dbRecordConflict = {
            'emailExists': emailQuery is not None,
            'usernameExists': usernameQuery is not None
        }
        if True in dbRecordConflict.values():
            print(f"There is a record containing username, and/or email: {dbRecordConflict}")
            return { 'error': True, 'message': dbRecordConflict }
        else:
            firstName, lastName, password = user['firstName'], user['lastName'], user['password']
            newUser = User(firstName, lastName, username, email, getHashedPass(password))
            db.session.add(newUser)
            db.session.commit()
            print(f"newly created user: {newUser}")
            return {'error': False, 'message': f'new user id: {newUser.id}'}
    else:
        return {'error': True, 'message': 'invalid payload'}


def signInUser(user):
    if None not in user.values():
        email, password = user['email'], user['password']
        userQuery = User.query.filter_by(email=email).first()
        signInErrors = {
            'userNotFound': userQuery is None,
            'passwordInvalid': False
        }
        if signInErrors['userNotFound']:
            return { 'error': True, 'message': signInErrors }
        else:
            savedPassword = userQuery.password
            signInErrors['passwordInvalid'] = not bcrypt.checkpw(password.encode(), savedPassword.encode())
            if signInErrors['passwordInvalid']:
                return { 'error': True, 'message': signInErrors }
            else:
                sessionToken = generateSessionToken({'user': getSignInPayload(userQuery)})
                print(f'token: {sessionToken}')
                response = make_response({
                    'error': False,
                    'token': sessionToken,
                    'data': getSignInPayload(userQuery)
                })
                response.headers['Authorization'] = f'Bearer {sessionToken}'
                return response


def getHashedPass(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf8')


def generateSessionToken(user):
    return create_access_token(identity=user)


def getSignInPayload(query):
    return {
        'id': query.id,
        'firstName': query.first_name,
        'username': query.username
    }


def resolveGlobalId(graphqlId):
    return from_global_id(graphqlId)[1]
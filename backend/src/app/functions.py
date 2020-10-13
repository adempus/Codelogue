"""
Contains app functionality for the app's features. Most of these functions are invoked via API routes.
"""
from graphql_relay.node.node import from_global_id
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_manager, verify_jwt_in_request
from flask import make_response, jsonify
from .models import User
from .setup import db
import bcrypt


# def signUpUser(user):
#     if None not in user.values():
#         email, username = user['email'].strip(), user['username'].strip()
#         emailQuery = User.query.filter_by(email=email).first()
#         usernameQuery = User.query.filter_by(username=username).first()
#         dbRecordConflict = {
#             'emailExists': emailQuery is not None,
#             'usernameExists': usernameQuery is not None
#         }
#         if True in dbRecordConflict.values():
#             print(f"There is a record containing username, and/or email: {dbRecordConflict}")
#             return { 'error': True, 'message': dbRecordConflict }
#         else:
#             firstName, lastName, password = user['firstName'], user['lastName'], user['password']
#             newUser = User(firstName, lastName, username, email, getHashedPass(password))
#             db.session.add(newUser)
#             db.session.commit()
#             print(f"newly created user: {newUser}")
#             return {'error': False, 'message': f'new user id: {newUser.id}'}
#     else:
#         return {'error': True, 'message': 'invalid payload'}

# def signInUser(user):
#     if None not in user.values():
#         email, password = user['email'], user['password']
#         userQuery = User.query.filter_by(email=email).first()
#         signInErrors = {
#             'userNotFound': userQuery is None,
#             'passwordInvalid': False
#         }
#         if signInErrors['userNotFound']:
#             return { 'error': True, 'message': signInErrors }
#         else:
#             savedPassword = userQuery.password
#             signInErrors['passwordInvalid'] = not bcrypt.checkpw(password.encode(), savedPassword.encode())
#             if signInErrors['passwordInvalid']:
#                 return { 'error': True, 'message': signInErrors }
#             else:
#                 sessionToken = generateSessionToken({'user': getSignInPayload(userQuery)})
#                 print(f'token: {sessionToken}')
#                 response = make_response({
#                     'error': False,
#                     'token': sessionToken,
#                     'data': getSignInPayload(userQuery)
#                 })
#                 response.headers['Authorization'] = f'Bearer {sessionToken}'
#                 return response


def signUp(firstName, lastName, username, email, password):
    dbRecordConflict = {
        'emailExists': User.query.filter_by(email=email).first() is not None,
        'usernameExists':  User.query.filter_by(username=username).first() is not None
    }
    if True in dbRecordConflict.values():
        return { 'error': True, 'message': "There is a record containing username and/or email", **dbRecordConflict }
    else:
        newUser = User(
            first_name=firstName, last_name=lastName,
            username=username, email=email,
            password=getHashedPass(password)
        )
        db.session.add(newUser)
        db.session.commit()
        return {'error': False, 'message': f'User sign up successful', 'user': newUser }


def signIn(email, password):
    userQuery = User.query.filter_by(email=email).first()
    signInErrors = {
        'userNotFound': userQuery is None,
        'passwordInvalid': False
    }
    if signInErrors['userNotFound']:
        return {'error': True, 'message': "No user found with this email", **signInErrors }
    else:
        savedPassword = userQuery.password
        signInErrors['passwordInvalid'] = not bcrypt.checkpw(password.encode(), savedPassword.encode())
        if signInErrors['passwordInvalid']:
            return {'error': True, 'message': "Password is invalid", **signInErrors }
        else:
            sessionToken = generateSessionToken({'user': getSignInPayload(userQuery)})
            response = {
                'message': 'Sign in successful',
                'error': False,
                'token': sessionToken,
            }
            return response


def getHashedPass(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf8')


def generateSessionToken(user):
    return create_access_token(identity=user)


def resolveUserId():
    user = get_jwt_identity()
    return user['user']['id']


def isResourceMatch(object):
    userId = resolveUserId()
    resMatch = object.user_id == userId
    if not resMatch:
        raise Exception('Resource accessed does not belong to user')
    return resMatch


def getSignInPayload(query):
    return {
        'id': query.id,
        'username': query.username
    }


def resolveGlobalId(graphqlId):
    return from_global_id(graphqlId)[1]



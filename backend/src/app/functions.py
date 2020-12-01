"""
 Contains basic functionality for the app's features, invoked through the API
"""
from graphql_relay.node.node import from_global_id
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, jwt_manager, verify_jwt_in_request, decode_token,
    get_raw_jwt
)
from flask import make_response, jsonify
from pendulum import from_timestamp, period, now
from .models import User
from .setup import db
import bcrypt


def signUp(username, email, password):
    dbRecordConflict = {
        'emailExists': User.query.filter_by(email=email).first() is not None,
        'usernameExists':  User.query.filter_by(username=username).first() is not None
    }
    if True in dbRecordConflict.values():
        return { 'error': True, 'message': "There is a record containing username and/or email", **dbRecordConflict }
    else:
        newUser = User(
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
            user = {'user': getSignInPayload(userQuery)}
            sessionToken = create_access_token(identity=user, fresh=True)
            refreshToken = create_refresh_token(identity=user)
            response = {
                'message': 'Sign in successful',
                'error': False,
                'access_token': sessionToken,
                'refresh_token': refreshToken
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


def getSessionDetails():
    tokenInfo =  get_raw_jwt()
    elapsedTime = period(now(), from_timestamp(tokenInfo['exp']))
    return {
        'session_start': from_timestamp(tokenInfo['iat']),
        'session_end': from_timestamp(tokenInfo['exp']),
        'time_remaining': elapsedTime.seconds,
    }
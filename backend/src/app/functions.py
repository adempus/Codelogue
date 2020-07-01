"""
Contains app functionality for the app's features. Most of these functions are invoked via API routes.
"""
from flask_jwt_extended import create_access_token
from .models import User
from .setup import db
import bcrypt


def signUpUser(user):
    if None not in user.values():
        email, username = user['email'], user['username']
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


def getHashedPass(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def generateSessionToken(user):
    return create_access_token(identity=user)


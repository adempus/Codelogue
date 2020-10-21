import json
import pytest
import inspect
from flask import request
from pprint import pprint as pp
from graphene.test import Client
from .api_calls import graphqlApi
from main import appData, app


testUser1 = {
    'firstName': 'Steve',
    'lastName': 'O\'Reilly',
    'username': 'soreilly1',
    'email': 'soreilly1@usda.gov',
    'password': 'tuHINTTAhag8'
}
testUser2 = {
    'firstName': 'Gracie',
    'lastName': 'Hudson',
    'username': 'g_hud99',
    'email': 'ghudson99@youku.com',
    'password': 'v4FrrGcWTZUAYMJBw'
}
pytest.signInResponse = None
pytest.client = Client(appData['schema'])
pytest.validToken = ""
pytest.expiredToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDIxOTk0NjMsIm5iZiI6MTYwMjE5OTQ2Mywian" \
                      "RpIjoiNmE3NTdhMTMtYzVjYS00ZDBjLWEyZjAtMTY3ZDdlMTE5YmJhIiwiZXhwIjoxNjAyMjAxNTYzLCJpZGVudGl0eSI6" \
                      "eyJ1c2VyIjp7ImlkIjoyLCJ1c2VybmFtZSI6InNxdWFuZG8ifX0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.7" \
                      "btYgCgEPUMPI0zFkWmOXq2UmfM-Uy_SElIh4Yv0qZQ"


def makeApiRequest(gqlApiCall, variables=None, accessToken=None):
    if accessToken:
        reqContext = app.test_request_context(headers={'Authorization': f'Bearer {accessToken}'})
        reqContext.push()
        with reqContext:
            response = pytest.client.execute(gqlApiCall, variables=variables)
    else:
        response = pytest.client.execute(gqlApiCall, variables=variables)
    print(f"\n~~ {inspect.stack()[1].function} result ~~\n")
    print(json.dumps(response, indent=4))
    return response


class TestUserSignUp:
    @pytest.mark.skip()
    def testSuccessfulUserSignUp(self):
        signUpResponse = makeApiRequest(graphqlApi['signUpMutation'], variables=testUser2)
        assert signUpResponse['data']['createUser']['__typename'] == 'UserSignUpSuccessOutput'
        assert signUpResponse['data']['createUser']['error'] == False
        assert 'user' in signUpResponse['data']['createUser'].keys()

    def testSignUpWithExistingCredentials(self):
        signUpResponse = makeApiRequest(graphqlApi['signUpMutation'], variables=testUser1)
        assert signUpResponse['data']['createUser']['__typename'] == 'UserSignUpErrorOutput'
        assert signUpResponse['data']['createUser']['error'] == True
        assert 'user' not in signUpResponse['data']['createUser'].keys()


class TestUserSignIn:
    def testUserSignInWithInvalidPassword(self):
        signInResponse = makeApiRequest(
            graphqlApi['signInMutation'],
            variables={'email': testUser1['email'], 'password': 'incorrect password attempt'}
        )
        assert signInResponse['data']['signInUser']['__typename'] == 'UserSignInErrorOutput'
        assert signInResponse['data']['signInUser']['error'] == True
        assert signInResponse['data']['signInUser']['passwordInvalid'] == True

    def testUserSignInWithInvalidEmail(self):
        signInResponse = makeApiRequest(
            graphqlApi['signInMutation'],
            variables={'email': 'invalidEmail@attempt.com', 'password': 'password'}
        )
        assert signInResponse['data']['signInUser']['__typename'] == 'UserSignInErrorOutput'
        assert signInResponse['data']['signInUser']['error'] == True
        assert signInResponse['data']['signInUser']['userNotFound'] == True

    # @pytest.mark.skip()
    def testSuccessfulUserSignIn(self):
        pytest.signInResponse = makeApiRequest(
            graphqlApi['signInMutation'],
            variables={'email': testUser1['email'], 'password': testUser1['password'] }
        )
        assert pytest.signInResponse['data']['signInUser']['__typename'] == 'UserSignInSuccessOutput'
        assert pytest.signInResponse['data']['signInUser']['error'] == False
        assert pytest.signInResponse['data']['signInUser']['accessToken'] is not None
        pytest.validToken = pytest.signInResponse['data']['signInUser']['accessToken']


class TestUserAuthentication:
    # @pytest.mark.skip()
    def testSuccessfulUserAuthAccess(self):
        authResponse = makeApiRequest(graphqlApi['checkAuthMutation'], accessToken=pytest.validToken)
        assert authResponse['data']['checkAuthorization']['error'] == False
        assert 'user' in authResponse['data']['checkAuthorization']

    def testExpiredUserAuthAccess(self):
        authResponse = makeApiRequest(graphqlApi['checkAuthMutation'], accessToken=pytest.expiredToken)
        assert authResponse['data']['checkAuthorization']['error'] == True
        assert 'user' not in authResponse['data']['checkAuthorization']

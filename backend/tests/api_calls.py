graphqlApi = {
    "signUpMutation":
        '''mutation ($email: String!, $firstName: String!, $lastName: String!, $password: String!, $username: String!) {
            createUser(email: $email, firstName: $firstName, lastName: $lastName, username: $username, password: $password) {
                __typename
                ...on UserSignUpErrorOutput {
                    error
                    message
                    emailExists
                    usernameExists
                }
                ...on UserSignUpSuccessOutput {
                    error
                    message
                    user {
                        id
                        username
                        email
                    }
                }   
            }
        }''',
    "signInMutation":
        '''mutation ($email: String!, $password: String!) {
            signInUser(email: $email, password: $password) {
                __typename
                ...on UserSignInErrorOutput {
                    error
                    message
                    userNotFound
                    passwordInvalid
                }
                ...on UserSignInSuccessOutput {
                    error
                    message
                    accessToken
                    refreshToken
                }
            }
        }''',
    "queryUsers":
        '''query {
            allUsers {
                edges {
                    node {
                        id
                        username
                        email
                    }
                }
            }
        }''',
    "queryUserFolders":
        '''query {
            getUserFolders {
                id
                name
            }
        }''',
    "checkAuthMutation":
        '''mutation {
            checkAuthorization {
                ...on AuthorizationErrorOutput {
                    __typename
                    error
                    message
                    tokenExpired
                    tokenInvalid
                }
                ...on AuthorizationSuccessOutput {
                    __typename
                    error
                    message
                    user {
                        id
                        username
                        email
                    }
                }
            }
        }''',
}

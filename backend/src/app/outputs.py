import graphene
from .objects import UserObject

class StatusOutput(graphene.Interface):
    error = graphene.Boolean()
    message = graphene.String()

class UserSignUpErrorOutput(graphene.ObjectType):
    class Meta:
        interfaces = (StatusOutput, )

    emailExists = graphene.Boolean()
    usernameExists = graphene.Boolean()

class UserSignUpSuccessOutput(graphene.ObjectType):
    class Meta:
        interfaces = (StatusOutput, )
    user = graphene.Field(UserObject)

class SignUpUserPayload(graphene.Union):
    class Meta:
        types = (UserSignUpSuccessOutput, UserSignUpErrorOutput, )


class UserSignInErrorOutput(graphene.ObjectType):
    class Meta:
        interfaces = (StatusOutput, )

    userNotFound = graphene.Boolean()
    passwordInvalid = graphene.Boolean()

class UserSignInSuccessOutput(graphene.ObjectType):
    class Meta:
        interfaces = (StatusOutput, )

    token = graphene.String()

class SignInUserPayload(graphene.Union):
    class Meta:
        types = (UserSignInErrorOutput, UserSignInSuccessOutput)


class AuthorizationErrorOutput(graphene.ObjectType):
    class Meta:
        interfaces = (StatusOutput, )

    tokenExpired = graphene.Boolean()
    tokenInvalid = graphene.Boolean()

class AuthorizationSuccessOutput(graphene.ObjectType):
    class Meta:
        interfaces = (StatusOutput, )
    user = graphene.Field(UserObject)

class AuthPayload(graphene.Union):
    class Meta:
        types = (AuthorizationErrorOutput, AuthorizationSuccessOutput)



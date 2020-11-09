"""
 Contains mutation classes for creating, upating, and deleting modeled GraphQL API resources (CUD in CRUD).
"""

import graphene
import pendulum
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, verify_jwt_in_request, get_jwt_identity, jwt_manager, create_access_token,
    decode_token, get_raw_jwt,
)
from .setup import db
from .objects import UserObject, FolderObject, SnippetObject, TagObject, TaggedSnippetObject
from .models import User, Folder, Snippet, Tag, TaggedSnippets
from .inputs import CreateSnippetInput, UpdateSnippetInput
from .outputs import *
import src.app.functions as functions
from sqlalchemy import func


class StatusField(graphene.ObjectType):
    error = graphene.Boolean()
    message = graphene.String()


class CheckAuthorization(graphene.Mutation):
    Output = AuthPayload
    def mutate(self, info):
        try:
            verify_jwt_in_request()
            details = functions.getSessionDetails()
            user = User.query.filter_by(id=functions.resolveUserId()).first()
        except jwt_manager.ExpiredSignatureError as ex:
            return AuthorizationErrorOutput(error=True, message=f"{ex}", tokenExpired=True)
        except jwt_manager.InvalidTokenError as ex:
            return AuthorizationErrorOutput(error=True, message=f"{ex}", tokenInvalid=True)
        return AuthorizationSuccessOutput(error=False, message="authentication valid", user=user, **details)


class RefreshAuthorization(graphene.Mutation):
    newToken = graphene.String()

    @jwt_refresh_token_required
    def mutate(self, info):
        user = get_jwt_identity()
        newToken = create_access_token(identity=user, fresh=False)
        return RefreshAuthorization(newToken=newToken)


''' User mutations '''

class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    Output = SignUpUserPayload

    def mutate(self, info, first_name, last_name, username, email, password):
        response = functions.signUp(first_name, last_name, username, email, password)
        if response['error']:
            return UserSignUpErrorOutput(error=response.pop('error'), message=response.pop('message'), **response)
        return UserSignUpSuccessOutput(error=response['error'], message=response['message'], user=response['user'])


class SignInUser(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    Output = SignInUserPayload

    def mutate(self, info, email, password):
        response = functions.signIn(email, password)
        if response['error']:
            return UserSignInErrorOutput(**response)
        return UserSignInSuccessOutput(**response)


class UpadteUserPassword(graphene.Mutation):
    user = graphene.Field(lambda: UserObject)
    status = graphene.Field(StatusField)
    class Arguments:
        user_id = graphene.ID(required=True)
        new_password = graphene.String(required=True)

    def mutate(self, info, user_id, new_password):
        userId = functions.resolveGlobalId(user_id)
        user = db.session.query(User).filter_by(id=userId)
        user.update({'password': functions.getHashedPass(new_password)})
        db.session.commit()
        return UpadteUserPassword(status=StatusField(error=False, message="Password change successful"))


''' Folder mutations '''

class CreateFolder(graphene.Mutation):
    folder = graphene.Field(lambda: FolderObject)
    status = graphene.Field(StatusField)
    class Arguments:
        name = graphene.String(description="Name of the folder", required=True)

    @jwt_required
    def mutate(self, info, name):
        userId = functions.resolveUserId()
        dateCreated = pendulum.now().to_datetime_string()
        folder = Folder(name=name, user_id=userId, date_created=dateCreated)
        db.session.add(folder)
        db.session.commit()
        return CreateFolder(folder=folder, status=StatusField(error=False, message="Folder created."))


class UpdateFolder(graphene.Mutation):
    folder = graphene.Field(lambda: FolderObject)
    status = graphene.Field(StatusField)
    class Arguments:
        folder_id = graphene.ID(required=True)
        name = graphene.String(required=True)

    @jwt_required
    def mutate(self, info, **input):
        folderId = functions.resolveGlobalId(input.pop('folder_id'))
        folder = db.session.query(Folder).filter_by(id=folderId).first()
        if functions.isResourceMatch(folder):
            db.session.query(Folder).filter_by(id=folderId).update(input)
            db.session.commit()
            folder = db.session.query(Folder).filter_by(id=folderId).first()
            return UpdateFolder(folder=folder, status=StatusField(error=False, message="Folder update successful"))


class DeleteFolder(graphene.Mutation):
    folder = graphene.Field(lambda: FolderObject)
    status = graphene.Field(StatusField)
    class Arguments:
        folder_id = graphene.ID(required=True)

    @jwt_required
    def mutate(self, info, folder_id):
        folderId = functions.resolveGlobalId(folder_id)
        folder = db.session.query(Folder).filter_by(id=folderId).first()
        if functions.isResourceMatch(folder):
            db.session.delete(folder)
            db.session.commit()
            return DeleteFolder(status=StatusField(error=False, message="Folder delete successful"))


''' Snippet mutations '''

class CreateSnippet(graphene.Mutation):
    snippet = graphene.Field(lambda: SnippetObject)
    status = graphene.Field(StatusField)
    class Arguments:
        input = CreateSnippetInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        userId = functions.resolveUserId()
        languageId = functions.resolveGlobalId(input['language_id'])
        folderId = functions.resolveGlobalId(input['folder_id'])
        dateCreated = pendulum.now().to_datetime_string()
        snippet = Snippet(
            user_id=userId, folder_id=folderId, language_id=languageId,
            title=input['title'], content=input['content'], description=input['description'],
            date_created=dateCreated
        )
        db.session.add(snippet)
        db.session.commit()
        return CreateSnippet(snippet=snippet, status=StatusField(error=False, message="Snippet creation successful"))


class UpdateSnippet(graphene.Mutation):
    snippet = graphene.Field(lambda: SnippetObject)
    status = graphene.Field(StatusField)
    class Arguments:
        input = UpdateSnippetInput(required=True)

    @jwt_required
    def mutate(self, info, input):
        snippetId = functions.resolveGlobalId(input.pop('snippet_id'))
        snippet = db.session.query(Snippet).filter_by(id=snippetId).first()
        if functions.isResourceMatch(snippet):
            # transform string ids present in input, to integer values before insertion
            input.update({ k : functions.resolveGlobalId(v) for (k,v) in input.items() if 'id' in k.split('_') })
            db.session.query(Snippet).filter_by(id=snippetId).update(input)
            db.session.commit()
            snippet = db.session.query(Snippet).filter_by(id=snippetId).first()
            return UpdateSnippet(snippet=snippet, status=StatusField(error=False, message="Snippet update success."))


class DeleteSnippet(graphene.Mutation):
    snippet = graphene.Field(lambda: SnippetObject)
    status = graphene.Field(StatusField)
    class Arguments:
        snippet_id = graphene.ID(required=True, description="Global graphql ID of the snippet to delete")

    @jwt_required
    def mutate(self, info, snippet_id):
        snippetId = functions.resolveGlobalId(snippet_id)
        snippet = db.session.query(Snippet).filter_by(id=snippetId).first()
        snippetTitle = snippet.title
        if functions.isResourceMatch(snippet):
            db.session.delete(snippet)
            db.session.commit()
            return DeleteSnippet(status=StatusField(error=False, message=f'Successfully deleted { snippetTitle }'))


'''
    CreateTags is invoked after the CreateSnippet mutation returns sucessfully. Keywords in the tags section of the 
    Snippet form will be sent as arguments to this mutation, returning their ids to be included in the proceeding call
    to CreateTaggedSnippet mutation.
'''

class CreateTags(graphene.Mutation):
    tags = graphene.List(lambda: TagObject)
    class Arguments:
        keywords = graphene.List(required=True, of_type=graphene.String)

    @jwt_required
    def mutate(self, info, keywords):
        userId = functions.resolveUserId()
        tagList = []
        for keyword in keywords:
            tag = db.session.query(Tag).filter(func.lower(Tag.keyword) == func.lower(keyword)).first()
            if tag is None:
                newTag = Tag(user_id=userId, keyword=keyword)
                tagList.append(newTag)
                db.session.add(newTag)
                db.session.commit()
            else:
                tagList.append(tag)
        return CreateTags(tags=tagList)


class CreateTaggedSnippet(graphene.Mutation):
    taggedSnippet = graphene.Field(lambda: TaggedSnippetObject)
    class Arguments:
        snippet_id = graphene.ID(required=True)
        tag_ids = graphene.List(required=True, of_type=graphene.ID)

    @jwt_required
    def mutate(self, info, snippet_id, tag_ids):
        snippetId = functions.resolveGlobalId(snippet_id)
        for id in tag_ids:
            tagId = functions.resolveGlobalId(id)
            taggedSnippet = TaggedSnippets(snippet_id=snippetId, tag_id=tagId)
            db.session.add(taggedSnippet)
            db.session.commit()
        return CreateTaggedSnippet(taggedSnippet=taggedSnippet)


class DeleteTaggedSnippet(graphene.Mutation):
    status = graphene.Field(StatusField)
    class Arguments:
        snippet_id = graphene.ID(required=True)
        tag_id = graphene.ID(required=True)

    @jwt_required
    def mutate(self, info, snippet_id, tag_id):
        snippetId, tagId = functions.resolveGlobalId(snippet_id), functions.resolveGlobalId(tag_id)
        snippet = db.session.query(Snippet).filter_by(id=snippetId).first()
        if functions.isResourceMatch(snippet):
            taggedSnippet = db.session.query(TaggedSnippets).filter_by(snippet_id=snippetId, tag_id=tagId).first()
            db.session.delete(taggedSnippet)
            db.session.commit()
        return DeleteTaggedSnippet(
            status=StatusField(error=False, message=f'Successfully deleted tag id {tagId} from tagged snippet {snippetId},')
        )


class Mutation(graphene.ObjectType):
    signInUser = SignInUser.Field()
    checkAuthorization = CheckAuthorization.Field()
    refreshAuthorization = RefreshAuthorization.Field()
    # creations
    createUser = CreateUser.Field()
    createFolder = CreateFolder.Field()
    createSnippet = CreateSnippet.Field()
    createTags = CreateTags.Field()
    createTaggedSnippet = CreateTaggedSnippet.Field()
    # updates
    updateSnippet = UpdateSnippet.Field()
    updateFolder = UpdateFolder.Field()
    updateUserPassword = UpadteUserPassword.Field()
    # deletions
    deleteFolder = DeleteFolder.Field()
    deleteSnippet = DeleteSnippet.Field()
    deleteTaggedSnippet = DeleteTaggedSnippet.Field()


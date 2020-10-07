import graphene
import pendulum
from flask_jwt_extended import jwt_required
from .setup import db
from .objects import UserObject, FolderObject, SnippetObject, TagObject, TaggedSnippetObject
from .models import User, Folder, Snippet, Tag, TaggedSnippets
from .inputs import CreateSnippetInput, UpdateSnippetInput
import src.app.functions as functions

class StatusField(graphene.ObjectType):
    error = graphene.Boolean()
    message = graphene.String()


''' User mutations '''

class CreateUser(graphene.Mutation):
    status = graphene.Field(StatusField)
    emailExists = graphene.Boolean()
    usernameExists = graphene.Boolean()
    user = graphene.Field(lambda: UserObject)
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, first_name, last_name, username, email, password):
        response = functions.signUp(first_name, last_name, username, email, password)
        status = StatusField(error=response.pop('error'), message=response.pop('message'))
        if status.error:
            return CreateUser(**response, status=status)
        return CreateUser(user=response.pop('user'), status=status)


class SignInUser(graphene.Mutation):
    status = graphene.Field(StatusField)
    userNotFound = graphene.Boolean()
    passwordInvalid = graphene.Boolean()
    token = graphene.String()
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, password):
        response = functions.signIn(email, password)
        status = StatusField(error=response.pop('error'), message=response.pop('message'))
        return SignInUser(**response, status=status)


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
            input.update({ k: functions.resolveGlobalId(v) for (k,v) in input.items() if 'id' in k.split('_') })
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
            return DeleteSnippet(status=StatusField(error=False, message=f'Successfully deleted {snippetTitle}'))


'''Tag mutations'''

class CreateTags(graphene.Mutation):
    tag = graphene.Field(lambda: TagObject)
    class Arguments:
        keywords = graphene.List(required=True, of_type=graphene.String)

    @jwt_required
    def mutate(self, info, keywords):
        userId = functions.resolveUserId()
        for keyword in keywords:
            tag = Tag(user_id=userId, keyword=keyword)
            db.session.add(tag)
            db.session.commit()
        return CreateTags(tag=tag)


class CreateTaggedSnippets(graphene.Mutation):
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
        return CreateTaggedSnippets(taggedSnippet=taggedSnippet)


class Mutation(graphene.ObjectType):
    # creations
    createUser = CreateUser.Field()
    createFolder = CreateFolder.Field()
    createSnippet = CreateSnippet.Field()
    createTags = CreateTags.Field()
    createTaggedSnippets = CreateTaggedSnippets.Field()
    signInUser = SignInUser.Field()
    # updates
    updateSnippet = UpdateSnippet.Field()
    updateFolder = UpdateFolder.Field()
    updateUserPassword = UpadteUserPassword.Field()
    # deletions
    deleteFolder = DeleteFolder.Field()
    deleteSnippet = DeleteSnippet.Field()


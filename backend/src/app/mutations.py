import graphene
import pendulum
from .setup import db
from graphql_relay.node.node import from_global_id
from .objects import FolderObject, SnippetObject
from .models import Folder, Snippet


class CreateFolder(graphene.Mutation):
    folder = graphene.Field(lambda: FolderObject)
    class Arguments:
        name = graphene.String(description="Name of the folder", required=True)
        user_id = graphene.ID(required=True)

    def mutate(self, info, name, user_id):
        userId = from_global_id(user_id)[1]
        dateCreated = pendulum.now().to_datetime_string()
        folder = Folder(name=name, user_id=userId, date_created=dateCreated)
        db.session.add(folder)
        db.session.commit()
        return CreateFolder(folder=folder)


class CreateSnippet(graphene.Mutation):
    snippet = graphene.Field(lambda: SnippetObject)
    class Arguments:
        user_id = graphene.ID(required=True)
        folder_id = graphene.ID(required=False)
        language_id = graphene.ID(required=False)
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        description = graphene.String(required=False)

    def mutate(self, info, user_id, folder_id, language_id, title, content, description):
        user_id = from_global_id(user_id)[1]
        language_id = from_global_id(language_id)[1]
        folder_id = from_global_id(folder_id)[1]
        dateCreated = pendulum.now().to_datetime_string()
        snippet = Snippet(
            user_id=user_id, folder_id=folder_id, language_id=language_id,
            title=title, content=content, description=description,
            date_created=dateCreated
        )
        db.session.add(snippet)
        db.session.commit()
        return CreateSnippet(snippet=snippet)


class Mutation(graphene.ObjectType):
    createFolder = CreateFolder.Field()
    createSnippet = CreateSnippet.Field()

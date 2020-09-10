import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
import sqlalchemy
import pendulum
from .models import User, Snippet, ProgrammingLanguage, Folder, Tag
from .setup import db


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )

class SnippetObject(SQLAlchemyObjectType):
    class Meta:
        model = Snippet
        interfaces = (relay.Node, )

class ProgrammingLanguageObject(SQLAlchemyObjectType):
    class Meta:
        model = ProgrammingLanguage
        interfaces = (relay.Node, )

class FolderObject(SQLAlchemyObjectType):
    class Meta:
        model = Folder
        interfaces = (relay.Node, )

class TagObject(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (relay.Node, )


# noinspection PyMethodMayBeStatic,PyShadowingBuiltins
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)
    all_snippets = SQLAlchemyConnectionField(SnippetObject)
    all_languages = SQLAlchemyConnectionField(ProgrammingLanguageObject)
    all_folders = SQLAlchemyConnectionField(FolderObject)
    all_tags = SQLAlchemyConnectionField(TagObject)
    # retrieve a specific user
    get_user = graphene.Field(UserObject, id=graphene.ID())
    # retrieve snippets by user_id
    get_user_snippets = graphene.Field(lambda: graphene.List(SnippetObject), user_id=graphene.ID())
    get_snippet_by_language = graphene.Field(lambda: graphene.List(SnippetObject),
                                             user_id=graphene.ID(),
                                             language_id=graphene.ID())
    # retrieve a list of folders by user_id
    get_user_folders = graphene.Field(lambda: graphene.List(FolderObject), user_id=graphene.ID())
    # resolver for user retrievals
    def resolve_get_user(self, info,  id):
        query = UserObject.get_query(info)
        return query.filter(User.id == id).first()

    def resolve_get_user_snippets(self, info, user_id):
        query = SnippetObject.get_query(info)
        return query.filter(Snippet.user_id == user_id).all()

    def resolve_get_snippet_by_language(self, info, user_id, language_id):
        query = SnippetObject.get_query(info)
        return query.filter(sqlalchemy.and_(Snippet.user_id == user_id, Snippet.language_id == language_id))

    def resolve_get_user_folders(self, info, user_id):
        query = FolderObject.get_query(info)
        return query.filter(Folder.user_id == user_id).all()


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


schema = graphene.Schema(query=Query, mutation=Mutation)


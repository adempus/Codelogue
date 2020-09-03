from .models import User, Snippet, ProgrammingLanguage, Folder, Tag
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import sqlalchemy


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
    # retrieve a specific snippet by user_id
    get_snippet = graphene.Field(SnippetObject, user_id=graphene.ID())
    get_snippet_by_language = graphene.Field(lambda: graphene.List(SnippetObject),
                                             user_id=graphene.ID(),
                                             language_id=graphene.ID())
    # retrieve a list of folders by user_id
    get_folders = graphene.Field(lambda: graphene.List(FolderObject), user_id=graphene.ID())
    # resolver for user retrieval
    def resolve_get_user(self, info,  id):
        query = UserObject.get_query(info)
        return query.filter(User.id == id).first()

    def resolve_get_snippet(self, info, user_id):
        query = SnippetObject.get_query(info)
        return query.filter(Snippet.user_id == user_id).first()

    def resolve_get_snippet_by_language(self, info, user_id, language_id):
        query = SnippetObject.get_query(info)
        return query.filter(sqlalchemy.and_(Snippet.user_id == user_id, Snippet.language_id == language_id))

    def resolve_get_folders(self, info, user_id):
        query = FolderObject.get_query(info)
        return query.filter(Folder.user_id == user_id).all()

schema = graphene.Schema(query=Query)


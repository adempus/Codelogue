import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import sqlalchemy
from .objects import *
from . import functions


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)
    all_snippets = SQLAlchemyConnectionField(SnippetObject)
    all_languages = SQLAlchemyConnectionField(ProgrammingLanguageObject)
    all_folders = SQLAlchemyConnectionField(FolderObject)
    all_tags = SQLAlchemyConnectionField(TagObject)
    # retrieve a specific user
    get_user = graphene.Field(UserObject, id=graphene.ID())
    # retrieve user snippets
    get_user_snippets = graphene.Field(lambda: graphene.List(SnippetObject), user_id=graphene.ID())
    # retrieve user snippets by language
    get_snippet_by_language = graphene.Field(
        lambda: graphene.List(SnippetObject),
        user_id=graphene.ID(),
        language_id=graphene.ID()
    )
    # retrieve a list of folders by user_id
    get_user_folders = graphene.Field(lambda: graphene.List(FolderObject), user_id=graphene.ID())
    # retrieve user tags
    get_user_tags = graphene.Field(lambda: graphene.List(TagObject), user_id=graphene.ID())
    get_all_tags = graphene.Field(lambda: graphene.List(TagObject))

    # resolver for user retrievals
    def resolve_get_user(self, info,  id):
        query = UserObject.get_query(info)
        return query.filter(User.id == id).first()

    def resolve_get_user_snippets(self, info, user_id):
        query = SnippetObject.get_query(info)
        return query.filter(Snippet.user_id == functions.resolveGlobalId(user_id)).all()

    def resolve_get_snippet_by_language(self, info, user_id, language_id):
        query = SnippetObject.get_query(info)
        return query.filter(
            sqlalchemy.and_(
                Snippet.user_id == functions.resolveGlobalId(user_id),
                Snippet.language_id == functions.resolveGlobalId(language_id)
            )
        )

    def resolve_get_user_folders(self, info, user_id):
        query = FolderObject.get_query(info)
        return query.filter(Folder.user_id == functions.resolveGlobalId(user_id)).all()

    def resolve_get_user_tags(self, info, user_id):
        query = TagObject.get_query(info)
        return query.filter(Tag.user_id == user_id).all()

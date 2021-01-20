"""
 Contains a query class which defines methods for reading modeled GraphQL API data (R in CRUD).
"""


import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from flask_jwt_extended import jwt_required, fresh_jwt_required
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
    get_user = graphene.Field(UserObject)
    # retrieve user snippets
    get_user_snippets = graphene.Field(lambda: graphene.List(SnippetObject))
    # retrieve user snippet by id
    get_snippet_by_id = graphene.Field(lambda: graphene.List(SnippetObject), snippet_id=graphene.ID())
    get_snippets_by_folder = graphene.Field(lambda: graphene.List(SnippetObject), folder_id=graphene.ID())
    # retrieve user snippets by language
    get_snippet_by_language = graphene.Field(lambda: graphene.List(SnippetObject),language_id=graphene.ID())
    # retrieve a list of folders by user_id
    get_user_folders = graphene.Field(lambda: graphene.List(FolderObject))
    # retrieve a folder by folder_id
    get_folder_by_id = graphene.Field(lambda: graphene.List(FolderObject), folder_id=graphene.ID())
    # retrieve user tags
    get_user_tags = graphene.Field(lambda: graphene.List(TagObject))
    get_all_tags = graphene.Field(lambda: graphene.List(TagObject))

    # resolver for user retrievals
    @jwt_required
    def resolve_get_user(self, info):
        userId = functions.resolveUserId()
        query = UserObject.get_query(info)
        return query.filter(User.id == userId).first()

    @jwt_required
    def resolve_get_user_snippets(self, info):
        userId = functions.resolveUserId()
        query = SnippetObject.get_query(info)
        return query.filter(Snippet.user_id == userId).all()

    @jwt_required
    def resolve_get_snippet_by_id(self, info, snippet_id):
        userId = functions.resolveUserId()
        query = SnippetObject.get_query(info)
        return query.filter(
            sqlalchemy.and_(
                Snippet.user_id == userId,
                Snippet.id == functions.resolveGlobalId(snippet_id)
            )
        )

    @jwt_required
    def resolve_get_snippets_by_folder(self, info, folder_id):
        userId = functions.resolveUserId()
        query = SnippetObject.get_query(info)
        return query.filter(
            sqlalchemy.and_(
                Snippet.user_id == userId,
                Snippet.folder_id == functions.resolveGlobalId(folder_id)
            )
        )

    @jwt_required
    def resolve_get_folder_by_id(self, info, folder_id):
        userId = functions.resolveUserId()
        query = FolderObject.get_query(info)
        return query.filter(
            sqlalchemy.and_(
                Folder.user_id == userId,
                Folder.id == functions.resolveGlobalId(folder_id)
            )
        )

    @jwt_required
    def resolve_get_snippet_by_language(self, info, language_id):
        print("in snippet language resolver")
        userId = functions.resolveUserId()
        query = SnippetObject.get_query(info)
        return query.filter(
            sqlalchemy.and_(
                Snippet.user_id == userId,
                Snippet.language_id == functions.resolveGlobalId(language_id)
            )
        )

    @jwt_required
    def resolve_get_user_folders(self, info):
        userId = functions.resolveUserId()
        query = FolderObject.get_query(info)
        return query.filter(Folder.user_id == userId).order_by(
            Folder.date_created.asc()
        ).all()

    @jwt_required
    def resolve_get_user_tags(self, info):
        userId = functions.resolveUserId()
        query = TagObject.get_query(info)
        return query.filter(Tag.user_id == userId).all()

    @jwt_required
    def resolve_get_all_tags(self, info):
        query = TagObject.getQuery(info)
        pass

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User, Snippet, ProgrammingLanguage, Folder, Tag, TaggedSnippets


class SnippetObject(SQLAlchemyObjectType):
    class Meta:
        model = Snippet
        interfaces = (relay.Node, )

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
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

class TaggedSnippetObject(SQLAlchemyObjectType):
    class Meta:
        model = TaggedSnippets
        interfaces = (relay.Node, )

import graphene
import pendulum
from .setup import db
from graphql_relay.node.node import from_global_id
from .objects import FolderObject, SnippetObject, TagObject, TaggedSnippetObject
from .models import Folder, Snippet, Tag, TaggedSnippets


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
        snippetTags = graphene.List(required=False, of_type=graphene.String)

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


class CreateTags(graphene.Mutation):
    tag = graphene.Field(lambda: TagObject)
    class Arguments:
        user_id = graphene.ID(required=True)
        keywords = graphene.List(required=True, of_type=graphene.String)

    def mutate(self, info,  user_id, keywords):
        user_id = from_global_id(user_id)[1]
        for keyword in keywords:
            tag = Tag(user_id=user_id, keyword=keyword)
            db.session.add(tag)
            db.session.commit()
        return CreateTags(tag=tag)


class CreateTaggedSnippets(graphene.Mutation):
    taggedSnippet = graphene.Field(lambda: TaggedSnippetObject)
    class Arguments:
        snippet_tag_ids = graphene.List(required=True, of_type=graphene.JSONString)

    def mutate(self, info, snippet_tag_ids):
        for idPair in snippet_tag_ids:
            print(f"snippet tag pair: {idPair}")
            tag_id = from_global_id(idPair['tag_id'])[1]
            snippet_id = from_global_id(idPair['snippet_id'])[1]
            taggedSnippet = TaggedSnippets(tag_id=tag_id, snippet_id=snippet_id)
            db.session.add(taggedSnippet)
            db.session.commit()
        return CreateTaggedSnippets(taggedSnippet=taggedSnippet)


class Mutation(graphene.ObjectType):
    createFolder = CreateFolder.Field()
    createSnippet = CreateSnippet.Field()
    createTags = CreateTags.Field()
    createTaggedSnippets = CreateTaggedSnippets.Field()

import graphene
import pendulum
from .setup import db
from .objects import FolderObject, SnippetObject, TagObject, TaggedSnippetObject
from .models import Folder, Snippet, Tag, TaggedSnippets
import src.app.functions as functions


''' Folder mutations '''

class CreateFolder(graphene.Mutation):
    folder = graphene.Field(lambda: FolderObject)
    class Arguments:
        name = graphene.String(description="Name of the folder", required=True)
        user_id = graphene.ID(required=True)

    def mutate(self, info, name, user_id):
        userId = functions.resolveGlobalId(user_id)
        dateCreated = pendulum.now().to_datetime_string()
        folder = Folder(name=name, user_id=userId, date_created=dateCreated)
        db.session.add(folder)
        db.session.commit()
        return CreateFolder(folder=folder)

class UpdateFolder(graphene.Mutation):
    folder = graphene.Field(lambda: FolderObject)
    class Arguments:
        folder_id = graphene.ID(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, **input):
        folderId = functions.resolveGlobalId(input.pop('foler_id'))
        folder = db.session.query(Folder).filter_by(id=folderId)
        folder.update(input)
        db.session.commit()
        folder = db.session.query(Folder).filter_by(id=folderId).first()
        return UpdateFolder(folder)

class DeleteFolder(graphene.Mutation):
    folder = graphene.Field(lambda: FolderObject)
    class Arguments:
        folder_id = graphene.ID(required=True)

    def mutate(self, info, folder_id):
        folderId = functions.resolveGlobalId(folder_id)
        folder = db.session.query(Folder).filter_by(id=folderId).first()
        db.session.delete(folder)
        db.session.commit()
        return DeleteFolder(folder)


''' Snippet mutations '''

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
        userId = functions.resolveGlobalId(user_id)
        languageId = functions.resolveGlobalId(language_id)
        folderId = functions.resolveGlobalId(folder_id)
        dateCreated = pendulum.now().to_datetime_string()
        snippet = Snippet(
            user_id=userId, folder_id=folderId, language_id=languageId,
            title=title, content=content, description=description,
            date_created=dateCreated
        )
        db.session.add(snippet)
        db.session.commit()
        return CreateSnippet(snippet=snippet)

class UpdateSnippet(graphene.Mutation):
    snippet = graphene.Field(lambda: SnippetObject)
    class Arguments:
        snippet_id = graphene.ID(required=True, description="Global graphql ID of the snippet")
        folder_id = graphene.ID(required=False)
        language_id = graphene.ID(required=False)
        title = graphene.String(required=False)
        content = graphene.String(required=False)
        description = graphene.String(required=False)
        snippetTags = graphene.List(required=False, of_type=graphene.String)

    def mutate(self, info, **input):
        snippetId = functions.resolveGlobalId(input.pop('snippet_id'))
        snippet = db.session.query(Snippet).filter_by(id=snippetId)
        snippet.update(input)
        db.session.commit()
        snippet = db.session.query(Snippet).filter_by(id=snippetId).first()
        return UpdateSnippet(snippet)

class DeleteSnippet(graphene.Mutation):
    snippet = graphene.Field(lambda: SnippetObject)
    class Arguments:
        snippet_id = graphene.ID(required=True, description="Global graphql ID of the snippet to delete")

    def mutate(self, info, snippet_id):
        snippetId = functions.resolveGlobalId(snippet_id)
        snippet = db.session.query(Snippet).filter_by(id=snippetId).first()
        db.session.delete(snippet)
        db.session.commit()
        return DeleteSnippet(snippet)


'''Tag mutations'''

class CreateTags(graphene.Mutation):
    tag = graphene.Field(lambda: TagObject)
    class Arguments:
        user_id = graphene.ID(required=True)
        keywords = graphene.List(required=True, of_type=graphene.String)

    def mutate(self, info,  user_id, keywords):
        userId = functions.resolveGlobalId(user_id)
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
    createFolder = CreateFolder.Field()
    createSnippet = CreateSnippet.Field()
    createTags = CreateTags.Field()
    createTaggedSnippets = CreateTaggedSnippets.Field()
    # updates
    updateSnippet = UpdateSnippet.Field()
    updateFolder = UpdateFolder.Field()
    # deletions
    deleteFolder = DeleteFolder.Field()
    deleteSnippet = DeleteSnippet.Field()

import graphene

''' This file contains input objects expected for mutations containing a common set of attributes. '''

class SnippetAttribute:
    folder_id = graphene.ID(required=False)
    language_id = graphene.ID(required=False)
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    description = graphene.String(required=False)
    snippetTags = graphene.List(required=False, of_type=graphene.String)

class CreateSnippetInput(graphene.InputObjectType, SnippetAttribute):
    # attribute needed to create a snippet
    user_id = graphene.ID(required=True)

class UpdateSnippetInput(graphene.InputObjectType, SnippetAttribute):
    # attribute needed to modify a snippet
    snippet_id = graphene.ID(required=True, description="Global graphql ID of the snippet")
    title = graphene.String(required=False)
    content = graphene.String(required=False)





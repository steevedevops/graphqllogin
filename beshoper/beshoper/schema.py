import graphene
from userapp.graphql.mutations import AuthMutation
from userapp.graphql.queries import UserQuery

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(mutation=Mutation, query=Query)

import graphene

from .graphql.query import Query
from .graphql.mutations import Mutation
from .graphql.objects import UserObject, ProfileObject, BlogObject

schema = graphene.Schema(query=Query, mutation=Mutation)
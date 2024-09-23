import graphene

from .graphql.query import Query
from .graphql.mutations import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
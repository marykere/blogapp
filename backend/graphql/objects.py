import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import User as UserModel, \
    Profile as ProfileModel, \
    Blog as BlogModel

class UserObject(SQLAlchemyObjectType):
   user_id = graphene.Int(source='id')

   class Meta:
       model = UserModel
       interfaces = (relay.Node, )

class ProfileObject(SQLAlchemyObjectType):
   class Meta:
       model = ProfileModel
       interface = (relay.Node, )


class BlogObject(SQLAlchemyObjectType): #added a BlogObject
   class Meta:
       model = BlogModel
       interface = (relay.Node, )

   title = graphene.String()  #added part: defined the fields
   body_content = graphene.String()

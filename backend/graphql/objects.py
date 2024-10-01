import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import User as UserModel, \
    Profile as ProfileModel, \
    Blog as BlogModel

class UserObject(SQLAlchemyObjectType):
    user_id = graphene.Int(source='id')
    is_suspended = graphene.Boolean()  # Add is_suspended field
    profile = graphene.Field(lambda: ProfileObject)  # Add profile relationship

    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class ProfileObject(SQLAlchemyObjectType):
    # first_name = graphene.String(required=True)
    # last_name = graphene.String(required=True)
    # user_id = graphene.Int(required=True)
    class Meta:
       model = ProfileModel
       interfaces = (relay.Node, )


class BlogObject(SQLAlchemyObjectType):
    title = graphene.String()
    body_content = graphene.String()  # Add the Text body content as a string
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    image_url = graphene.String()  # Add the image_url field

    class Meta:
        model = BlogModel
        interfaces = (relay.Node, )



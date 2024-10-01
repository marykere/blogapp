import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from ..models import Profile as ProfileModel, \
   User as UserModel, \
   Blog as BlogModel

#, \
   #Role as RoleModel

from ..graphql.objects import UserObject as User, \
   ProfileObject as Profile, \
   BlogObject as Blog


class Query(graphene.ObjectType):
   node = relay.Node.Field()

   users = graphene.List(
       lambda: User, email=graphene.String(), user_id=graphene.Int())


   def resolve_users(self, info, email=None):
       query = User.get_query(info)
       #query = info.context.session.query(UserModel)

       if email:
           query = query.filter(UserModel.email == email)
       return query.all()
   
   profiles = graphene.List(
       lambda: Profile, id=graphene.Int())

   def resolve_profiles(self, info, id=None):
       query = Profile.get_query(info)
       #query = info.context.session.query(ProfileModel) 

       if id:
           query = query.filter(
               ProfileModel.id == id)
       return query.all()
   
   blogs = graphene.List(
       lambda: Blog, body_content=graphene.String())

   def resolve_blogs(self, info, body_content = None):
       query = Blog.get_query(info)
       #query = info.context.session.query(BlogModel) 

       if body_content:
           query = query.filter(
               BlogModel.body_content == body_content)
       return query.all()
   
   def resolve_create_blog(self, user, info, **kwargs): #this part is added for user suspension
       query = User.get_query(info)
       #query = info.context.session.query(UserModel)

       if user.is_suspended:
           raise Exception ("Your Account has been suspended")
           query = query.filter(
               BlogModel.body_content == body_content)
       return query.all()

   all_users = SQLAlchemyConnectionField(User)
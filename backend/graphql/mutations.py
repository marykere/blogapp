import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from backend import db
from ..graphql.objects import UserObject as User, \
    ProfileObject as Profile, \
    BlogObject as Blog

from ..models import User as UserModel, \
    Profile as ProfileModel, \
    Blog as BlogModel
    



class UserMutation(graphene.Mutation):
   class Arguments:
       email = graphene.String(required=True)
       password = graphene.String(required=True)
       first_name = graphene.String(required=True)
       last_name = graphene.String(required=True)

   user = graphene.Field(lambda: User)

   def mutate(self, info, email, password, first_name, last_name):
        # Create the profile
        profile = Profile(first_name=first_name, last_name=last_name)
        db.session.add(profile)
        db.session.commit()

        # Create the user
        user = User(email=email, profile_id=profile.id)
        user.set_password(password)  # Hash the password
        db.session.add(user)
        db.session.commit()
        return UserMutation(user=user)


class ProfileMutation(graphene.Mutation):
   class Arguments:
       first_name = graphene.String(required=True)
       last_name = graphene.String(required=True)
       user_id = graphene.Int(required=True)

   profile = graphene.Field(lambda: Profile)

   def mutate(self, info, first_name, last_name, user_id):
       user = UserModel.query.get(user_id)

       profile = ProfileModel(first_name=first_name, last_name=last_name)

       db.session.add(profile)

       user.profile = profile
       db.session.commit()

       return ProfileMutation(profile=profile)

 #creating a section for the blog mutation 

class BlogMutation(graphene.Mutation): 
    class Arguments:
        body_content = graphene.String(required=True)
        title = graphene.String(required=True)
        image_url=graphene.String()
        user_id = graphene.Int(required=True)

    blog = graphene.Field(lambda: Blog)

    #def mutate(self, info, title, body_content, user_id, first_name, last_name):
    def mutate(self, info, title, body_content, user_id, image_url=None):
        # Fetch the user
        user = User.query.get(user_id)
        if user.is_suspended:
            raise Exception("Your account has been suspended.")
        
        # Create blog post
        blog = Blog(title=title, body_content=body_content, image_url=image_url, user_id=user.id)
        db.session.add(blog)
        db.session.commit()

        return BlogMutation(blog=blog)
    

class Mutation(graphene.ObjectType):
   mutate_user = UserMutation.Field()
   mutate_profile = ProfileMutation.Field()
   mutate_blog = BlogMutation.Field()
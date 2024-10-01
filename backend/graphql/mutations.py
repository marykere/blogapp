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
    #    user_id = graphene.Int(required=True)
       email = graphene.String(required=True)
       password = graphene.String(required=True)
       first_name = graphene.String(required=True)
       last_name = graphene.String(required=True)

   user = graphene.Field(lambda: User)
   success = graphene.Boolean()
   message = graphene.String()

   def mutate(self, info, email, password, first_name, last_name):
        #confirms that required fields are filled
        if not email or not first_name or not last_name:
          raise Exception("Required fields Must be filled")
        
        # Check if the user already exists
        existing_user = UserModel.query.filter_by(email=email).first()
        if existing_user:
          raise Exception("User Already Exists.") #added a validation for when a user already exists
        
        if existing_user and existing_user.check_and_suspend_user():
            raise Exception("Your account has been suspended due to inactivity.")
        
        #existing_user.check_and_suspend_user()

        # Create the profile
        profile = ProfileModel(first_name=first_name, last_name=last_name)
        db.session.add(profile)
        db.session.commit()

    
        # Create the user and associate it with the created profile
        new_user = UserModel(email=email, profile_id=profile.id)
        new_user.set_password(password)  # Hash the password

        db.session.add(new_user)
        db.session.commit()


        return UserMutation(user=new_user, success = True, message="User created successfully")


class ProfileMutation(graphene.Mutation):
   class Arguments:
       first_name = graphene.String(required=True)
       last_name = graphene.String(required=True)
       user_id = graphene.Int(required=True)

   profile = graphene.Field(lambda: Profile)

   def mutate(self, info, first_name, last_name, user_id):
       user = UserModel.query.get(user_id)

       profile = ProfileModel(first_name=first_name, last_name=last_name)

       #user.check_and_suspend_user() #unsure if this should stay
        

       db.session.add(profile)

       user.profile = profile
       db.session.commit()

       return ProfileMutation(profile=profile)

 #creating a section for the blog mutation 

class BlogMutation(graphene.Mutation): 
    class Arguments:
        user_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        body_content = graphene.String(required=True)
        image_url=graphene.String()

    blog = graphene.Field(lambda: Blog)

    def mutate(self, info, user_id, title, body_content, image_url=None):
        # Fetch the user
        user = UserModel.query.get(user_id)
        if not user:
          raise Exception("User Does not Exist.")
        if user:
          raise Exception("User Already Exists.") #added a validation for when a user already exists

        
        # Create blog post
        blog = BlogModel(title=title, body_content=body_content, image_url=image_url, user_id=user.id)
        db.session.add(blog)
        db.session.commit()

        return BlogMutation(blog=blog)
    

class Mutation(graphene.ObjectType):
   mutate_user = UserMutation.Field()
   mutate_profile = ProfileMutation.Field()
   mutate_blog = BlogMutation.Field()
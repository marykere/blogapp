import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from backend import db
from ..graphql.objects import UserObject as User, \
    ProfileObject as Profile, \
    BlogObject as Blog
from flask_bcrypt import Bcrypt
from flask_login import login_user
from flask_mail import Message, Mail

from ..models import User as UserModel, \
    Profile as ProfileModel, \
    Blog as BlogModel
mail=Mail()   
from marshmallow import ValidationError, validate


class UserMutation(graphene.Mutation):
   class Arguments:
    #    user_id = graphene.Int(required=True)
       email = graphene.String(required=True)
       password = graphene.String(required=True)

       def validate_password(self, password): #setting up a field for validating my password 
          if len(password) < 8:
             raise ValidationError("Password Must be at least 8 characters long!")
          elif not any(char.isdigit() for char in password):
             raise ValidationError("Password Must contain at least 1 special character")
          elif not any(char.isUpper() for char in password):
             raise ValidationError("At least 1 character should be uppercase")
          
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
        new_user.set_password(password)  #hash the password

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
    
      
bcrypt = Bcrypt()

class LoginMutation(graphene.Mutation):
   class Arguments:
      email = graphene.String(required=True)
      password = graphene.String(required=True)

   success = graphene.Boolean()
   error = graphene. String()

   def mutate(self, info, email, password):
        user = UserModel.query.filter_by(email=email).first()
        if not user or not user.check_password: #this is defined in the models.py file
            return LoginMutation(success=False, error="Invalid username or password!")

        login_user(user)
        return LoginMutation(success=True)


class RequestPasswordReset(graphene.Mutation):
   class Arguments:
      username=graphene.String()
      email=graphene.String()

   error = graphene.String()

   def mutate(self, info, user, email):
      user=UserModel.query.filter_by(email=email).first()
      if user:
         token = user.get_reset_token()
         msg= Message('Password Reset Request',
                     sender='marykere20@gmail.com',
                     recipients=[user.email])
         msg.body=f'''To reset your password, follow the following link:
         http://yourdomain.com/reset_password/{token} 
If you did not make this request, please ignore this email.

'''
         mail.send(msg)
      
      else:
         RequestPasswordReset(error='Wrong email or password entered!')

class PasswordReset(graphene.Mutation):
   class Arguments:
      email=graphene.String()
      new_password=graphene.String()
      confirm_new_password=graphene.String()

   success=graphene.Boolean()
   message=graphene.String()

   def mutate(self, info, email, new_password, confirm_new_password):
      user=UserModel.query.filter_by(email=email).first()

      if not user:
         return PasswordReset(success=False, message='User does not exist. If new user, please create an account.')
      elif new_password != confirm_new_password:
         return PasswordReset(success=False, message='Password fields do not match!')
      
      hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
      user.password = hashed_password
      db.query.commit()

      return PasswordReset(success=True, message='Your password has been reset successfully. Kindly login to your account.')
    

class Mutation(graphene.ObjectType):
   mutate_user = UserMutation.Field()
   mutate_profile = ProfileMutation.Field()
   mutate_blog = BlogMutation.Field()
   mutate_login = LoginMutation.Field()
   password_reset_request=RequestPasswordReset.Field()
   mutate_password=PasswordReset.Field()
from backend import db
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, JSON
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(
       db.String(64), unique=True, index=True)

   #THIS IS NEW BELOW
   profile_id = db.Column(
       db.Integer, db.ForeignKey('profiles.id'))

   profile = db.relationship(
       "Profile", backref='user')
   password_hash = db.Column(
        db.String(64), unique=True, nullable=False)
   def set_password(self, password): 
        self.password_hash = generate_password_hash(password)

   def check_password(self, password):
        return check_password_hash(self.password_hash)
   is_suspended = db.Column(db.Boolean, default=False)

   def __repr__(self):
       return f"<User {self.email} >"


class Profile(db.Model):
   __tablename__ = 'profiles'
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(20))
   last_name = db.Column(db.String(20))
   

   def __repr__(self):
       return f"<Profile {self.first_name} {self.last_name}: #{self.id} >"
   
class Blog(db.Model):
   __tablename__ = 'blogs'
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(20),
                    index=True, nullable=False)
   body_content = db.Column(db.Text, nullable=False) #change made from type Text to type JSON
   created_at = db.Column(DateTime, default=datetime.now()) #added a timestamp for when a user creates and updates a blog
   updated_at = db.Column (DateTime, onupdate=datetime.now()) #removed parentheses for datetime.now() to see if it works
   image_url=db.Column(db.String(255), nullable=True) #this part is added for when a user wants to add an image

   def __repr__(self):
       return f"<Blog {self.title} {self.body_content}>"
   
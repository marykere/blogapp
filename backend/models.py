from backend import db
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, DateTime, JSON
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(
       db.String(64), unique=True, index=True, nullable=False) #email cannot be empty

   #THIS IS NEW BELOW
   profile_id = db.Column(
       db.Integer, db.ForeignKey('profiles.id'))
   password_hash = db.Column(
        db.String(256), unique=True, nullable=False)
   def set_password(self, password): 
        self.password_hash = generate_password_hash(password)

   def check_password(self, password):
        return check_password_hash(self.password_hash)
   is_suspended = db.Column(db.Boolean, default=False)
   def check_and_suspend_user(self):
       if datetime.now() - self.profile.logged_in_time > timedelta(days=30): #added a suspend user field 
           self.is_suspended=True
   profile = db.relationship(
       "Profile", backref='user')
   blogs = db.relationship('Blog', back_populates='user')


   def __repr__(self):
       return f"<User {self.email} >"


class Profile(db.Model):
   __tablename__ = 'profiles'
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(20), nullable=False)
   last_name = db.Column(db.String(20), nullable=False)
   created_at = db.Column(db.DateTime, default=datetime.now())
   logged_in_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now()) #added a field for when a user created (&logged into)their profile
   

   def __repr__(self):
       return f"<Profile {self.first_name} {self.last_name}: #{self.id} >"
   
class Blog(db.Model):
   __tablename__ = 'blogs'
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(20),
                    index=True, nullable=False)
   body_content = db.Column(db.Text, nullable=False) #change made from type Text to type JSON (undone)
   created_at = db.Column(db.DateTime, default=datetime.now()) #added a timestamp for when a user creates and updates a blog
   updated_at = db.Column (db.DateTime, onupdate=datetime.now()) #removed parentheses for datetime.now() to see if it works
   image_url=db.Column(db.String(255), nullable=True) #this part is added for when a user wants to add an image
   user_id = Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Ensure this line exists

   user = db.relationship('User', back_populates='blogs')


   def __repr__(self):
       return f"<Blog {self.title} {self.body_content}>"
   
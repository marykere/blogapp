from backend import db

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
   body_content = db.Column(
       db.Text, nullable=False)

   def __repr__(self):
       return f"<Blog {self.title} {self.body_content}>"
   
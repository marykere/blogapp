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
   skills = db.relationship("Skill")

   def __repr__(self):
       return f"<Profile {self.first_name} {self.last_name}: #{self.id} >"


class Skill(db.Model):
   __tablename__ = 'skills'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20), unique=True,
                    index=True, nullable=False)
   profile_id = db.Column(
       db.Integer, db.ForeignKey('profiles.id'))

   def __repr__(self):
       return f"<Skill {self.name} >"
   
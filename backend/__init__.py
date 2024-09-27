from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow #this part is added 
from config import config  
#this part is added 
from flask_jwt_extended import JWTManager 
from flask_migrate import Migrate 

from flask_graphql import GraphQLView

db = SQLAlchemy( )
jwt=JWTManager()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    from .api import api as api_blueprint  
    app.register_blueprint(api_blueprint, url_prefix='/api/')

    from .schema import schema

    app.add_url_rule(
       '/graphql',
       view_func=GraphQLView.as_view(
           'graphql',
           schema=schema,
           graphiql=True  # for having the GraphiQL interface
       )
   )

    return app


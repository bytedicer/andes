from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity

from resources.user import UserRegister
from resources.blueprint import BlueprintList, BlueprintCreate, Blueprint
from resources.service import ServiceList, ServiceCreate, Service
from resources.stack import StackList, StackCreate, Stack, StackApply
from resources.network import NetworkList, NetworkCreate, Network


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3000)
app.secret_key = "DEVELOPMENT_KEY"
api = Api(app)
jwt = JWT(app, authenticate, identity)

# @app.before_first_request
# def create_tables():
#   db.create_all()

api.add_resource(UserRegister, '/register')

api.add_resource(BlueprintList, '/blueprints')
api.add_resource(BlueprintCreate, '/blueprints/create')
api.add_resource(Blueprint, '/blueprints/<int:_id>')

api.add_resource(ServiceList, '/services')
api.add_resource(ServiceCreate, '/services/create')
api.add_resource(Service, '/services/<int:_id>')

api.add_resource(StackList, '/stacks')
api.add_resource(StackCreate, '/stacks/create')
api.add_resource(Stack, '/stacks/<int:_id>')
api.add_resource(StackApply, '/stacks/<int:_id>/apply')

api.add_resource(NetworkList, '/networks')
api.add_resource(NetworkCreate, '/networks/create')
api.add_resource(Network, '/networks/<int:_id>')

if __name__ == "__main__":
  from db import db
  db.init_app(app)
  app.run(host='127.0.0.1', port=5000, debug=True)

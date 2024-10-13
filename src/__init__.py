from flask import Flask
from flask_restful import Resource, Api

from model import db
from auth import login_manager, UserRegister, UserLogin, Logout, bcrypt, Protected
from follow import FollowUser, UnfollowUser

app = Flask(__name__)
app.secret_key = 'super secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

api = Api(app)

db.app = app
db.init_app(app)

login_manager.init_app(app)
bcrypt.init_app(app)


### Create the Database ###
with app.app_context():
    db.create_all()
    
class HelloWorld(Resource):
    
    def get(self):
        return {'hello':'world'}

api.add_resource(HelloWorld,'/')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(Logout, '/logout')
api.add_resource(Protected,'/protected')
api.add_resource(FollowUser,'/follow')
api.add_resource(UnfollowUser,'/unfollow')

if __name__ == '__main__':
    app.run(debug=True)

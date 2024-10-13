from flask import request
from flask_restful import Resource, abort
from model.usermodel import User
from flask_login import login_required, current_user
from model import db

class FollowUser(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        follower = User(current_user)
        followed = User.query.filter_by(id=data.get('user_followed')).first()

        if not followed:
            abort(400, message='User does not exist!')

        follower.follow(followed)
      
class UnfollowUser(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        follower = User(current_user)
        followed = User.query.filter_by(id=data.get('user_followed')).first()

        if not followed:
            abort(400, message='User does not exist!')
        
        follower.unfollow(followed)
        
from flask import request
from flask_restful import Resource, abort
from model.usermodel import User
from flask_login import login_user, logout_user, LoginManager, login_required
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import re
from model import db

bcrypt = Bcrypt()
login_manager = LoginManager()

def validateRegistration(username, email, pw):
    if not validators.email(email): 
        abort(400, message='email address not valid!')
    
    if User.query.filter_by(email=email).first():
        abort(400, message="email address already in use!")
        
    if User.query.filter_by(username=username).first():
        abort(400, message ="username already in use!")


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
       
        validateRegistration(username, email, password) 

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, email=email, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        
        return {
            'message':'user created!',
            'username': username,
            'email': email
        }, 201


@login_manager.user_loader
def userLoader(userID):
    User.query.get(int(userID))

class UserLogin(Resource):
    def post(self):
        data = request.get_json()       
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
           abort(400, message='No account associated with this email address!') 

        if not bcrypt.check_password_hash(user.password, password):
            abort(400, message='password is wrong!')

        login_user(user)

        return {
            'message':'user logged in successfully!'
        },200

class Logout(Resource):
    
    @login_required
    def get(self):
        logout_user()
        return {"message": "Logged out successfully"}, 200
        
class Protected(Resource):
    @login_required
    def get(self):
        return {'message': 'This is a protected route'}
        
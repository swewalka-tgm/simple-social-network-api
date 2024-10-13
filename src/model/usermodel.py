from model import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship to represent who the user is following
    following = db.relationship(
        'User', secondary='followers',
        primaryjoin='User.id == followers.c.follower_id',
        secondaryjoin='User.id == followers.c.followed_id',
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(
            followers.c.followed_id == user.id).count() > 0

# Followers Association Table (Join Table)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('followed_at', db.DateTime, default=datetime.now)
)
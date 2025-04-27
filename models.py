from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from models import User, Post, Comment, Like, Interest, UserInterest, Follow
    db.create_all()

# You can paste your CREATE TABLE logic here as SQLAlchemy models later

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    posts = db.relationship('Post', back_populates='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)
    likes = db.relationship('Like', back_populates='user', lazy=True)
    interests = db.relationship('UserInterest', back_populates='user', lazy=True)

    # Define the relationships with Follow
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', back_populates='followed', lazy=True)
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower', lazy=True)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', lazy=True)
    likes = db.relationship('Like', back_populates='post', foreign_keys='Like.post_id', lazy=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')
    likes = db.relationship('Like', back_populates='comment', foreign_keys='Like.comment_id')

class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'), nullable=True)

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes', foreign_keys=[post_id])
    comment = db.relationship('Comment', back_populates='likes', foreign_keys=[comment_id])



class Interest(db.Model):
    interest_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    user_interests = db.relationship('UserInterest', back_populates='interest', lazy=True)


class UserInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.interest_id'), nullable=False)

    user = db.relationship('User', back_populates='interests')
    interest = db.relationship('Interest', back_populates='user_interests')


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # These are the reverse relationships
    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers')


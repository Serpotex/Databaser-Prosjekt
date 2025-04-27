from app import app, db
from models import User, Post, Comment, Like, Interest, UserInterest, Follow
from sqlalchemy.exc import IntegrityError

# Run this inside an app context
with app.app_context():
    # Drop all existing tables (if needed)
    db.drop_all()

    # Create all tables based on models
    db.create_all()

    # Add some sample data to the database
    try:
        # Add users
        user1 = User(username="john_doe", email="john@example.com")
        user2 = User(username="jane_doe", email="jane@example.com")
        db.session.add(user1)
        db.session.add(user2)
        
        # Add interests
        interest1 = Interest(name="Programming")
        interest2 = Interest(name="AI")
        db.session.add(interest1)
        db.session.add(interest2)
        
        # Commit users and interests
        db.session.commit()

        # Create relationships (User Interests)
        user_interest1 = UserInterest(user_id=user1.user_id, interest_id=interest1.interest_id)
        user_interest2 = UserInterest(user_id=user2.user_id, interest_id=interest2.interest_id)
        db.session.add(user_interest1)
        db.session.add(user_interest2)

        # Create posts
        post1 = Post(content="Loving Flask for web development!", user_id=user1.user_id)
        post2 = Post(content="AI is revolutionizing the world!", user_id=user2.user_id)
        db.session.add(post1)
        db.session.add(post2)

        # Create comments
        comment1 = Comment(content="Absolutely agree, Flask is awesome!", post_id=post1.post_id, user_id=user2.user_id)
        db.session.add(comment1)

        # Add likes
        like1 = Like(post_id=post1.post_id, user_id=user2.user_id)
        db.session.add(like1)

        # Commit all changes
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    print("Sample data added successfully!")

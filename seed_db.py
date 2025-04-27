from app import app, db
from models import User, Follow, Post, Comment, Like, Interest, UserInterest  # Import your models
from sqlalchemy.exc import IntegrityError
# Wipe the database (optional, for re-seeding)
with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    users = [
        User(username="alice", email="alice@example.com"),
        User(username="bob", email="bob@example.com"),
        User(username="carla", email="carla@example.com"),
        User(username="daniel", email="daniel@example.com"),
        User(username="elena", email="elena@example.com"),
        User(username="felix", email="felix@example.com"),
        User(username="george", email="george@example.com"),
        User(username="hannah", email="hannah@example.com"),
        User(username="iris", email="iris@example.com"),
        User(username="jack", email="jack@example.com"),
    ]
    db.session.add_all(users)
    db.session.commit()

    # Posts
    posts = [
        Post(user_id=1, content="Hello world!"),
        Post(user_id=2, content="Just had coffee ☕"),
        Post(user_id=3, content="Looking for book recommendations!"),
        Post(user_id=1, content="Flask is awesome 💻"),
        Post(user_id=4, content="Exploring Norway this summer."),
        Post(user_id=5, content="Studying for finals... send help 😩"),
        Post(user_id=6, content="Anyone up for gaming tonight?"),
        Post(user_id=7, content="Trying out a new recipe 🍝"),
        Post(user_id=8, content="Finished reading a great article on AI."),
        Post(user_id=9, content="Working on my social media project!"),
    ]
    db.session.add_all(posts)
    db.session.commit()

    # Comments
    comments = [
        Comment(post_id=1, user_id=2, content="Welcome!"),
        Comment(post_id=1, user_id=3, content="Hey Alice!"),
        Comment(post_id=2, user_id=4, content="What kind of coffee?"),
        Comment(post_id=3, user_id=1, content='Try "Sapiens" by Yuval Harari'),
        Comment(post_id=4, user_id=2, content="Same! Flask + Jinja2 rocks"),
        Comment(post_id=5, user_id=6, content="Visit Bergen!"),
        Comment(post_id=6, user_id=7, content="Good luck on finals!"),
        Comment(post_id=7, user_id=5, content="Send me the recipe!"),
        Comment(post_id=8, user_id=10, content="Link?"),
        Comment(post_id=9, user_id=3, content="Nice! I’m doing that too."),
    ]
    db.session.add_all(comments)
    db.session.commit()

    # Interests
    interests = [
        Interest(name="Technology"),
        Interest(name="Books"),
        Interest(name="Travel"),
        Interest(name="Cooking"),
        Interest(name="Gaming"),
        Interest(name="Fitness"),
        Interest(name="Education"),
        Interest(name="Music"),
        Interest(name="AI"),
        Interest(name="Nature"),
    ]
    db.session.add_all(interests)
    db.session.commit()

    # UserInterest
    user_interests = [
        UserInterest(user_id=1, interest_id=1), UserInterest(user_id=1, interest_id=2),
        UserInterest(user_id=2, interest_id=3), UserInterest(user_id=2, interest_id=4),
        UserInterest(user_id=3, interest_id=2), UserInterest(user_id=3, interest_id=7),
        UserInterest(user_id=4, interest_id=1), UserInterest(user_id=4, interest_id=9),
        UserInterest(user_id=5, interest_id=6), UserInterest(user_id=5, interest_id=10),
        UserInterest(user_id=6, interest_id=5), UserInterest(user_id=6, interest_id=4),
        UserInterest(user_id=7, interest_id=5), UserInterest(user_id=7, interest_id=3),
        UserInterest(user_id=8, interest_id=1), UserInterest(user_id=8, interest_id=9),
        UserInterest(user_id=9, interest_id=2), UserInterest(user_id=9, interest_id=1),
        UserInterest(user_id=10, interest_id=8), UserInterest(user_id=10, interest_id=2),
    ]
    db.session.add_all(user_interests)
    db.session.commit()

    # Follows
    follows = [
        Follow(follower_id=2, followed_id=1),
        Follow(follower_id=3, followed_id=1),
        Follow(follower_id=4, followed_id=2),
        Follow(follower_id=5, followed_id=3),
        Follow(follower_id=6, followed_id=4),
        Follow(follower_id=1, followed_id=5),
        Follow(follower_id=2, followed_id=6),
        Follow(follower_id=3, followed_id=7),
        Follow(follower_id=4, followed_id=8),
        Follow(follower_id=5, followed_id=9),
    ]
    db.session.add_all(follows)
    db.session.commit()

    # Likes
    likes = [
        Like(user_id=2, post_id=1),
        Like(user_id=3, post_id=1),
        Like(user_id=4, post_id=2),
        Like(user_id=5, post_id=3),
        Like(user_id=1, post_id=4),
        Like(user_id=6, post_id=4),
        Like(user_id=7, post_id=5),
        Like(user_id=8, post_id=6),
        Like(user_id=9, post_id=7),
        Like(user_id=10, post_id=9),
    ]
    db.session.add_all(likes)
    db.session.commit()

        # Likes on posts
    db.session.add_all([
        Like(user_id="alice.user_id", post_id="p2.post_id"),
        Like(user_id="bob.user_id", post_id="p1.post_id"),
        Like(user_id="charlie.user_id", post_id="p1.post_id"),
    ])

    # Likes on comments
    db.session.add_all([
        Like(user_id="alice.user_id", comment_id="c1.comment_id"),
        Like(user_id="charlie.user_id", comment_id="c1.comment_id"),
        Like(user_id="bob.user_id", comment_id="c2.comment_id"),
    ])
    db.session.commit()
    print("✅ Database seeded successfully!")

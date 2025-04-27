from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import text
from models import db, init_db, User, Post, Comment, Like, Interest, UserInterest, Follow


app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')



# CRUD SYSTEM
# USERS CRUD
@app.route('/users')
def list_users():
    print("list_users loaded")
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('form.html', action='Create User')

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

#POSTS CRUD
@app.route('/posts')
def list_posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts_with_likes) # posts=posts

@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        user_id = request.form['user_id']
        content = request.form['content']
        post = Post(user_id=user_id, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('list_posts'))
    users = User.query.all()
    return render_template('form.html', action='Create Post', users=users)

@app.route('/posts/delete/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('list_posts'))

# COMMENT CRUD
@app.route('/comments')
def list_comments():
    comments = Comment.query.all()
    return render_template('comments.html', comments=comments)

@app.route('/comments/create', methods=['GET', 'POST'])
def create_comment():
    if request.method == 'POST':
        post_id = request.form['post_id']
        user_id = request.form['user_id']
        content = request.form['content']
        comment = Comment(post_id=post_id, user_id=user_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('list_comments'))
    users = User.query.all()
    posts = Post.query.all()
    return render_template('form.html', action='Create Comment', users=users, posts=posts)

@app.route('/comments/delete/<int:comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('list_comments'))

@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    # Get the current logged-in user. For now, assuming user_id = 1
    current_user_id = 1  # Replace this with actual logic to get the current logged-in user's ID
    
    # Check if the user has already liked this post
    existing_like = Like.query.filter_by(user_id=current_user_id, post_id=post_id).first()
    if existing_like:
        # If the user already liked the post, don't add another like
        return redirect(url_for('posts'))
    
    # Add a like to the post
    like = Like(user_id=current_user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()

    # Redirect back to the comments or posts page
    return redirect(url_for('posts'))


#QUERIES
@app.route('/queries')
def queries():
    queries = {}

        # 1. Posts with authors
    queries["posts_with_authors"] = db.session.execute(text("""
        SELECT post.post_id, post.content, user.username
        FROM Post AS post
        JOIN User AS user ON post.user_id = user.user_id;
    """)).fetchall()

    queries["comments_info"] = db.session.execute(text("""
        SELECT comment.comment_id, comment.content AS comment_text, user.username AS commenter,
            post.content AS original_post,
            COUNT(like.like_id) AS total_likes
        FROM Comment AS comment
        JOIN User AS user ON comment.user_id = user.user_id
        JOIN Post AS post ON comment.post_id = post.post_id
        LEFT JOIN Like AS like ON comment.comment_id = like.comment_id
        GROUP BY comment.comment_id;
    """)).fetchall()

    # 3. Post count per user
    queries["post_count_per_user"] = db.session.execute(text("""
        SELECT user.user_id, user.username, COUNT(post.post_id) AS total_posts
        FROM User AS user
        LEFT JOIN Post AS post ON user.user_id = post.user_id
        GROUP BY user.user_id;
    """)).fetchall()


    # 4. Posts containing 'Flask'
    queries["posts_flask"] = db.session.execute(text("""
        SELECT * FROM Post
        WHERE content LIKE '%Flask%';
    """)).fetchall()

    # 5. Likes per post
    queries["likes_per_post"] = db.session.execute(text("""
        SELECT post.post_id, post.content, COUNT(like.like_id) AS total_likes
        FROM Post AS post
        LEFT JOIN Like AS like ON post.post_id = like.post_id
        JOIN User AS user ON post.user_id = user.user_id
        GROUP BY post.post_id;
    """)).fetchall()


    return render_template("queries.html", queries=queries)

if __name__ == '__main__':
    app.run(debug=True)

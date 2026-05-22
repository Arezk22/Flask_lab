from flask import Flask, redirect, render_template, request, url_for
from database import db
from config import POSTGRES_URI, MYSQL_URI
from models import Post , Comment
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def list_posts():
    posts = Post.query.order_by(Post.id.asc()).all()
    if not posts:
        return render_template('list_posts.html', posts=[])
    return render_template('list_posts.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':        
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '').strip()
        if not title or not content or not author:
            return 'Title, content, and author are required', 400
        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('list_posts'))
    return render_template('create_post.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    # post = Post.query.get_or_404(post_id)
    post = db.session.get(Post, post_id)
    if not post:
        return f'Post with ID {post_id} not found', 404
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '').strip()
        if not title or not content or not author:
            return 'Title, content, and author are required', 400
        post.title = title
        post.content = content
        post.author = author
        db.session.commit()
        return redirect(url_for('list_posts'))
    return render_template('update_post.html', post=post)

@app.route('/details/<int:post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    # post = Post.query.get_or_404(post_id)
    post = db.session.get(Post, post_id)
    if not post:
        return f'Post with ID {post_id} not found', 404
    if request.method=='POST':
        comment_author=request.form.get('comment_author', '').strip()
        comment_content=request.form.get('comment_content','').strip()
        if not comment_author or not comment_content:
            return 'Comment author and content are required', 400
        new_comment = Comment(
            author=comment_author, 
            content=comment_content, 
            post_id=post_id
        )
        db.session.add(new_comment)
        db.session.commit()    
        return redirect(url_for('post_details', post_id=post_id))    
    return render_template('detail_post.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # post = Post.query.get_or_404(post_id)
    post = db.session.get(Post, post_id)
    if not post:
        return f'Post with ID {post_id} not found', 404
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('list_posts'))

@app.route('/comments/<int:post_id>')
def post_comments(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return f'Post with ID {post_id} not found', 404
    comments = Comment.query.filter(Comment.post_id == post_id).order_by(Comment.id.asc()).all()
    print(comments)
    return render_template('comments.html', comments=comments, post=post)

if __name__ == '__main__':
    app.run(debug=True)
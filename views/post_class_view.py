from flask import Blueprint, render_template, request, redirect, url_for
from flask.views import MethodView
from database import db
from models import Post, Comment

posts_class_bp = Blueprint('posts_class', __name__)

class PostListCreateView(MethodView):
  def get(self):
    if request.path == '/create':
        return render_template('create_post.html')
    posts=Post.query.order_by(Post.id.asc()).all()
    return render_template('list_posts.html', posts=posts or [])

  def post(self):
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    author = request.form.get('author', '').strip()
    if not title or not content or not author:
      return 'Title, content, and author are required', 400
    new_post=Post(title=title,content=content,author=author)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('posts_class.list_create_view')) 

class PostDetailUpdateDeleteView(MethodView):
  def get(self , post_id):
    post = db.session.get(Post,post_id)
    if not post:
      return f'Post with ID {post_id} not found', 404
    
    if request.endpoint == 'posts_class.post_edit':
      return render_template('update_post.html', post=post)
    return render_template('detail_post.html', post=post)
  
  def post(self, post_id):
    post = db.session.get(Post, post_id)
    if not post:
      return f'Post with ID {post_id} not found', 404
    if request.endpoint == 'posts_class.post_details':
      comment_author = request.form.get('comment_author', '').strip()
      comment_content = request.form.get('comment_content', '').strip()
      if not comment_author or not comment_content:
        return 'Comment author and content are required', 400
      new_comment = Comment(author=comment_author, content=comment_content, post_id=post_id)
      db.session.add(new_comment)
      db.session.commit()
      return redirect(url_for('posts_class.post_details', post_id=post_id))

    elif request.endpoint == 'posts_class.post_edit':
      title = request.form.get('title', '').strip()
      content = request.form.get('content', '').strip()
      author = request.form.get('author', '').strip()
      if not title or not content or not author:
        return 'Title, content, and author are required', 400
      post.title = title
      post.content = content
      post.author = author
      db.session.commit()
      return redirect(url_for('posts_class.list_create_view'))
    elif request.endpoint == 'posts_class.post_delete':
      db.session.delete(post)
      db.session.commit()
      return redirect(url_for('posts_class.list_create_view'))
    return f'Unsupported action for endpoint {request.endpoint}', 400
    
class PostCommentsView(MethodView):
  def get(self, post_id):
        post = db.session.get(Post, post_id)
        if not post:
            return f'Post with ID {post_id} not found', 404
        comments = Comment.query.filter(Comment.post_id == post_id).order_by(Comment.id.asc()).all()
        return render_template('comments.html', comments=comments, post=post)
  def post(self, post_id):
    post = db.session.get(Post, post_id)
    if not post:
      return f'Post with ID {post_id} not found', 404
    comment_author = request.form.get('comment_author', '').strip()
    comment_content = request.form.get('comment_content', '').strip()
    if not comment_author or not comment_content:
      return 'Comment author and content are required', 400
    new_comment = Comment(author=comment_author, content=comment_content, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    # return redirect(url_for(''))
    return render_template('list_posts.html', post=post)

# class=object.as_view('endpoint_name')  
list_create_view = PostListCreateView.as_view('list_create_view')
detail_update_delete_view = PostDetailUpdateDeleteView.as_view('detail_update_delete_view')
comments_view = PostCommentsView.as_view('comments_view')

posts_class_bp.add_url_rule('/', view_func=list_create_view, methods=['GET', 'POST'])
posts_class_bp.add_url_rule('/create', view_func=list_create_view, methods=['GET', 'POST'])
posts_class_bp.add_url_rule('/details/<int:post_id>', view_func=detail_update_delete_view, methods=['GET', 'POST'], endpoint='post_details')
posts_class_bp.add_url_rule('/edit/<int:post_id>', view_func=detail_update_delete_view, methods=['GET', 'POST'], endpoint='post_edit')
posts_class_bp.add_url_rule('/delete/<int:post_id>', view_func=detail_update_delete_view, methods=['POST'], endpoint='post_delete')
posts_class_bp.add_url_rule('/comments/<int:post_id>', view_func=comments_view, methods=['GET'], endpoint='comments_view')
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from database import db
from models import Post, Comment

posts_api_bp = Blueprint('posts_api', __name__)

class PostListCreateAPI(MethodView):
    def get(self):
        posts = Post.query.order_by(Post.id.asc()).all()
        posts_data = [{
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'author': p.author
        } for p in posts]
        return jsonify(posts_data), 200

    def post(self):
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        author = data.get('author', '').strip()
        
        if not title or not content or not author:
            return jsonify({'error': 'Title, content, and author are required'}), 400
            
        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': {'id': new_post.id, 'title': new_post.title, 'author': new_post.author}
        }), 201

class PostDetailUpdateDeleteAPI(MethodView):
    def get(self, post_id):
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({'error': f'Post with ID {post_id} not found'}), 404
            
        comments = Comment.query.filter(Comment.post_id == post_id).order_by(Comment.id.asc()).all()
        comments_data = [{'id': c.id, 'author': c.author, 'content': c.content} for c in comments]

        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author,
            'comments': comments_data
        }), 200

    def put(self, post_id):
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({'error': f'Post with ID {post_id} not found'}), 404
            
        data = request.get_json() or {}
        post.title = data.get('title', post.title).strip()
        post.content = data.get('content', post.content).strip()
        post.author = data.get('author', post.author).strip()
        
        db.session.commit()
        return jsonify({'message': 'Post updated successfully'}), 200

    def delete(self, post_id):
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({'error': f'Post with ID {post_id} not found'}), 404
            
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': f'Post with ID {post_id} deleted successfully'}), 200

list_create_api = PostListCreateAPI.as_view('list_create_api')
detail_update_delete_api = PostDetailUpdateDeleteAPI.as_view('detail_update_delete_api')

posts_api_bp.add_url_rule('/posts', view_func=list_create_api, methods=['GET', 'POST'])
posts_api_bp.add_url_rule('/posts/<int:post_id>', view_func=detail_update_delete_api, methods=['GET', 'PUT', 'DELETE'])
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from database import db
from models import Post, Comment

posts_api_bp = Blueprint('posts_api', __name__)

users = [{
    'id':1,
    'name':'Ahmed Ali',
    'email':'ahmed.ali@example.com',
    'age':30
},
{
    'id':2,
    'name':'Mohamed Hassan',
    'email':'mohamed.hassan@example.com',
    'age':25
}
]

class UserAPI(MethodView):
    def get(self, user_id=None):
        if user_id is not None:
            user = next((u for u in users if u['id'] == user_id), None)
            if not user:
                return jsonify({'error': f'User with ID {user_id} not found'}), 404
            return jsonify(user), 200
        return jsonify(users), 200
    def post(self):
        data = request.get_json() or {}
        new_user = {
            'id': len(users) + 1,
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'age': data.get('age', 0)
        }
        users.append(new_user)
        return jsonify({'message': 'User created successfully', 'user': new_user}), 201
    def put(self, user_id):
        data = request.get_json() or {}
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        user['name'] = data.get('name', user['name'])
        user['email'] = data.get('email', user['email'])
        user['age'] = data.get('age', user['age'])
        return jsonify({'message': 'User updated successfully', 'user': user}), 200
        
    def delete(self, user_id):
        data = request.get_json() or {}
        user = next((u for u in users if u['id'] == user_id), None)
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        users.remove(user)
        return jsonify({'message': 'User deleted successfully'}), 200
    
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
user_api = UserAPI.as_view('user_api')

posts_api_bp.add_url_rule('/posts', view_func=list_create_api, methods=['GET', 'POST'])
posts_api_bp.add_url_rule('/posts/<int:post_id>', view_func=detail_update_delete_api, methods=['GET', 'PUT', 'DELETE'])
posts_api_bp.add_url_rule('/users', view_func=user_api, methods=['GET', 'POST'])
posts_api_bp.add_url_rule('/users/<int:user_id>', view_func=user_api, methods=['GET', 'PUT', 'DELETE'])

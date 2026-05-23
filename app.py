from flask import Blueprint, Flask, redirect, render_template, request, url_for
from database import db
from config import POSTGRES_URI, MYSQL_URI
from models import Post , Comment
from views.post_function_view import posts_func_bp
from views.post_class_view import posts_class_bp
from api.api import posts_api_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


app.register_blueprint(posts_class_bp, url_prefix='/posts')
app.register_blueprint(posts_api_bp, url_prefix='/api')
# app.register_blueprint(posts_func_bp)

if __name__ == '__main__':
    app.run(debug=True)
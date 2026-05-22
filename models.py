from database import db

class Post(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  author = db.Column(db.String(255), nullable=False)
  comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
  def __repr__(self):
    return f'<Post {self.id} - {self.title}>'
  

class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
  content = db.Column(db.Text, nullable=False)
  author = db.Column(db.String(255), nullable=False)
  # post = db.relationship('Post', backref=db.backref('comments', lazy=True))
  def __repr__(self):
    return f'<Comment {self.id} on Post {self.post_id}>'
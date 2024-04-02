from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/forum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    links = db.Column(db.Text, nullable=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'links': self.links,
            'comments': [comment.to_dict() for comment in self.comments]
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    links = db.Column(db.Text, nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'links': self.links,
            'post_id': self.post_id
        }

# API routes
@app.route('/', methods=["GET"])
def hello():
    return "Hello", 200

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    post = Post(title=data['title'], content=data['content'], image_url=data.get('image_url'), links=data.get('links'))
    db.session.add(post)
    db.session.commit()
    return jsonify({'post_id': post.post_id}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200

@app.route('/posts/comments/<int:post_id>', methods=['POST'])
def add_comment_to_post(post_id):
    data = request.json
    comment = Comment(title=data['title'], content=data['content'], post_id=post_id, image_url=data.get('image_url'), links=data.get('links'))
    db.session.add(comment)
    db.session.commit()
    return jsonify({'comment_id': comment.comment_id}), 201

@app.route('/posts/comments/<int:post_id>', methods=['GET'])
def get_comments_for_post(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify([comment.to_dict() for comment in comments]), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

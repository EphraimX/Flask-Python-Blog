from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
				'sqlite:///' + os.path.join(basedir, 'posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPost(db.Model):

	__tablename__ = 'BlogPost'
	id_num = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	author = db.Column(db.String(50), nullable=False, default='Unknown')
	date_posted = db.Column(db.DateTime, nullable = False, default=datetime.date(datetime.now()))

	def __repr__(self):
		return 'Blog Post' + str(self.id_num)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/posts', methods=['GET'])
def posts():
	all_post = BlogPost.query.order_by(BlogPost.date_posted).all()
	return render_template('post.html', posts=all_post)


@app.route('/posts/delete/<int:id>')
def delete(id):
	post = BlogPost.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
	edit_post = BlogPost.query.get_or_404(id)
	if request.method == 'POST':
		edit_post.title = request.form['title']
		edit_post.content = request.form['content']
		edit_post.author = request.form['author']
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('edit.html', post=edit_post)



@app.route('/posts/new', methods=['GET','POST'])
def new_post():
	if request.method == 'POST':
		new_post_title = request.form['title']
		new_post_content = request.form['content']
		new_post_author = request.form['author']
		new_post = BlogPost(title=new_post_title , content=new_post_content, author=new_post_author)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('new_post.html')




if __name__ == "__main__":
	app.run(debug=True)
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    blog_id = request.args.get('id') #bringing a 'dictionary' object

    if blog_id == None:   #if blog is not present
        posts = Blog.query.all() #get all post across a table
        return render_template('blog.html', posts=posts, title='Build-a-blog') # provide the name of the template and the variables you want to pass to the template engine as keyword arguments
    else: #if blog is present
        post = Blog.query.get(blog_id)  #getall post across table with id
        return render_template('entry.html', post=post, title='Blog Entry') #blog entry

@app.route('/newpost', methods=['POST', 'GET'])  #new post
def new_post():
    if request.method == 'POST': #post new entry
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
        title_error = ''
        body_error = ''

        if not blog_title: # if there is not a title
            title_error = "Please enter a blog title"
        if not blog_body: # if there is not a blog body
            body_error = "Please enter a blog entry"

        if not body_error and not title_error: # if both not available then create new and commit to database
            new_entry = Blog(blog_title, blog_body)     
            db.session.add(new_entry)
            db.session.commit()        
            return redirect('/blog?id={}'.format(new_entry.id)) 
        else: #send to create new post
            return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error, 
                blog_title=blog_title, blog_body=blog_body)
     
    return render_template('newpost.html', title='New Entry')

if  __name__ == "__main__":
    app.run()
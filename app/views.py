from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user
from app import app, db, lm
from .forms import LoginForm, RegisterForm, BlogForm
from .models import User, Post
from config import userCollection, postCollection
import hashlib
import functools

def login_required(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            if session.get('logged_in'):
                return fn(*args, **kwargs)
            return redirect(url_for('login', next=request.path))
        return inner

@app.route('/')
@app.route('/index')
#@login_required
def index():
    #user = g.user
    user = 'fusae'
    posts = [
                {
                    'author': {'nickname': 'John'},
                    'body': 'Beautiful day in Portland!'
                },

                {
                    'author': {'nickname': 'Susan'},
                    'body': 'The Avengers movie was so cool!'
                },
            ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    user_record = db[userCollection].find_one({'_id': id})
    if user_record:
        user = User(user_record['username'], user_record['password'], user_record['email'])
        return user
    else:
        return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    # register data, we should valid form data
    if form.validate_on_submit():
        username = form.username.data
        password = hashlib.md5(form.password.data.encode('utf-8')).hexdigest()
        email = form.email.data

        # check if the user has registered
        user = db[userCollection].find_one({'email': email, 'username': username})
        if user:
            # alread exist
            flash('user already exist')
            return render_template('register.html', form=form)

        user = User(username, password, email).toDict
        db[userCollection].insert(user)
        flash('user successfully registered') 
        return redirect(url_for('index'))
    return abort(400);

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    # login data, we should vaild form data
    if form.validate_on_submit():
        username = form.username.data
        password = hashlib.md5(form.password.data.encode('utf-8')).hexdigest() 
        register_user = db[userCollection].find_one({'username': username, 'password': password})
        if register_user is None:
            flash('username or password is invalid', 'error')
            return redirect(url_for('login'))
        logined_user = User(register_user['username'], form.password.data, register_user['email'])
        login_user(logined_user, remember=form.remember_me.data)
        flash('Logged in successfully')
        session['logged_in'] = True
        return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    form = BlogForm()
    if request.method == 'GET':
        return render_template('create_blog.html', form=form)
    # handle post data
    if form.validate_on_submit():
        post = Post(form.title.data, form.body.data)
        flash('post created successfully')
        post = post.toDict
        db[postCollection].insert(post) 
        return redirect(url_for('show_blog', blog_id=post['blog_id']))
    return abort(400)

@app.route('/blog/<blog_id>')
def show_blog(blog_id):
    post = db[postCollection].find_one({'blog_id': blog_id})
    return render_template('detail.html', post=post)

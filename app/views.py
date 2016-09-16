from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user
from app import app, db, lm
from .forms import LoginForm, RegisterForm, BlogForm
from .models import User, Post
from .pagination import Pagination
from config import userCollection, postCollection
import hashlib
import functools
import mistune
from flask import Markup

def login_required(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            if session.get('logged_in'):
                return fn(*args, **kwargs)
            return redirect(url_for('signin', next=request.path))
        return inner

@app.route('/')
#@app.route('/index')
#@app.route('/index/<int:page>')
#@login_required
#def index(page=1):
def index():
    
    page = 1 if not request.args.get('page') else int(request.args.get('page'))
    per_page = 1

    total = db[postCollection].count()
    pagination = Pagination(page, per_page, total, postCollection) 
    posts = pagination.getPage()
    
    return render_template("index.html",
                           title='Home',
                           posts=posts,
                           pagination=pagination)

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
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
            return render_template('signup.html', form=form)

        user = User(username, password, email).toDict
        db[userCollection].insert(user)
        flash('user successfully registered') 
        return redirect(url_for('index'))
    return abort(400);

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('signin.html', form=form)
    # login data, we should vaild form data
    if form.validate_on_submit():
        username = form.username.data
        password = hashlib.md5(form.password.data.encode('utf-8')).hexdigest() 
        register_user = db[userCollection].find_one({'username': username, 'password': password})
        if register_user is None:
            flash('username or password is invalid', 'error')
            return redirect(url_for('signin'))
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
    return redirect(url_for('signin'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_blog():
    form = BlogForm()
    if request.method == 'GET':
        return render_template('manage_blog.html', action='create_blog')
    # handle post data
    if form.validate_on_submit():
        url_title = form.url_title.data.replace(' ', '-')
        post = Post(form.title.data, url_title, form.abstract.data, form.content.data)
        flash('post created successfully')
        post = post.toDict
        db[postCollection].insert(post) 
        return redirect(url_for('show_blog', url_title=post['url_title']))
    return abort(400)

@app.route('/blog/<url_title>')
def show_blog(url_title):
    post = db[postCollection].find_one({'url_title': url_title})
    content = post['content']
    markdown = mistune.Markdown()
    post['content'] = Markup(markdown(content))
    logged_in = session['logged_in'] if session.get('logged_in') else False
    return render_template('post.html', post=post, logged_in=logged_in)


@login_required
@app.route('/edit/<url_title>', methods=['GET', 'POST'])
def edit_blog(url_title):
    form = BlogForm()
    post = db[postCollection].find_one({'url_title': url_title})

    if request.method == 'GET':
        return render_template('manage_blog.html', post=post, action='edit_blog')

    #if form.validate_on_submit():
    if request.method == 'POST':
        edit_post = Post(
                    request.form.get('title'),
                    request.form.get('url_title'),
                    request.form.get('abstract'),
                    request.form.get('content')
                )
        edit_post = edit_post.toDict
        edit_post['created_at'] = post['created_at']
        db[postCollection].update({'created_at': post['created_at']}, {'$set': edit_post}, upsert=False)
        return redirect(url_for('show_blog', url_title=edit_post['url_title']))

    return abort(400)


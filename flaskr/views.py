from functools import wraps
from flask import request, redirect, url_for, render_template, flash, abort, jsonify, session, g
from flaskr import app, db, data
from flaskr.models import Event, Entry, User, Category, Post

def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_view

@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])

@app.route('/')
@login_required
def calendar():
    empty_rooms = data.get_empty_rooms()
    for day, schedule in empty_rooms.items():
        for time in range(len(schedule)):
            empty_rooms[day][time] = len(schedule[time])
    return render_template('calendar.html', data=empty_rooms)

@app.route('/events/create/', methods=['GET', 'POST'])
def event_create():
    day=request.args.get('day')
    room=request.args.get('room')
    time=int(request.args.get('time'))
    if request.method == 'POST':
        category = request.form["category"]
        category = Category.query.filter(Category.name == category).first()
        event = Event(title=request.form['title'],
                      description=request.form['description'],
                      day=day,
                      room=room,
                      time=time
        )
        event.categories.append(category)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event_list'))
    return render_template('event/edit.html', day=day, room=room, time=time)

@app.route('/events/')
def event_list():
    events = Event.query.all()
    return render_template('event/list.html', events=events)

@app.route('/events/<int:event_id>/')
def event_detail(event_id, joined=False):
    event = Event.query.get(event_id)
    user_id = session.get('user_id')
    joined = User.query.get(user_id) in event.users
    event_time = str(int(event.time) + 1)
    return render_template('event/detail.html', event=event, event_time=event_time, joined=joined)

@app.route('/events/<int:event_id>/edit/', methods=['GET', 'POST'])
def event_edit(event_id):
    event = Event.query.get(event_id)
    if event is None:
        abort(404)
    if request.method == 'POST':
        event.title=request.form['title']
        event.description=request.form['description']
        event.day=request.form['day']
        event.room=request.form['room']
        event.time=request.form['time']
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event_detail', event_id=event_id))
    return render_template('event/edit.html', event=event)

@app.route('/events/<int:event_id>/delete/', methods=['DELETE'])
def event_delete(event_id):
    event = Event.query.get(event_id)
    if event is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(event)
    db.session.commit()
    return jsonify({'status': 'OK'})

@app.route("/plan")
def show_plan():
    day, time = request.args.get('day'), int(request.args.get('time'))
    room = request.args.get('room')
    empty_rooms = data.get_empty_rooms()
    empty_rooms = empty_rooms[day][time]
    events = data.get_event_rooms()
    events = events[day][time]
    return render_template('plan.html', empty_rooms=empty_rooms, events=events, room=room, day=day, time=time)

@app.route('/users/')
@login_required
def user_list():
    users = User.query.all()
    return render_template('user/list.html', users=users)

@app.route('/users/<int:user_id>/')
@login_required
def user_detail(user_id):
    user = User.query.filter(User.id == user_id).first()
    return render_template('user/detail.html', user=user)

@app.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if request.method == 'POST':
        user.name=request.form['name']
        category = request.form["category"]
        category = Category.query.filter(Category.name == category).first()
        user.categories.append(category)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    return render_template('user/edit.html', user=user)

@app.route('/users/create/', methods=['GET', 'POST'])
def user_create():
    if request.method == 'POST':
        user = User(name=request.form['name'])
        category = request.form["category"]
        category = Category.query.filter(Category.name == category).first()
        user.categories.append(category)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_list'))
    return render_template('user/edit.html')

@app.route('/users/<int:user_id>/delete/', methods=['DELETE'])
def user_delete(user_id):
    user = User.query.get(user_id)
    if user is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'OK'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.authenticate(db.session.query,
                request.form['name'])
        if user != None:
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('calendar'))
        else:
            flash('Invalid your name')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/event/<int:event_id>/join')
@login_required
def join_event(event_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    event = Event.query.get(event_id)
    user.events.append(event)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/posts/create/', methods=['GET', 'POST'])
def post_create():
    if request.method == 'POST':
        title = request.form["title"]
        body = request.form["body"]
        categories = request.form.getlist("categories")
        category_data = []
        for category in categories:
            tmp = Category.query.filter(Category.name == category).first()
            category_data.append(tmp)
        print(category_data)
        post = Post(title=title,
                    body=body
        )
        for category in category_data:
            post.categories.append(category)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post_list'))
    categories = Category.query.all()
    return render_template('post/edit.html', categories=categories)

@app.route('/posts/')
def post_list():
    posts = Post.query.all()
    print(posts[0].title)
    return render_template('post/list.html', posts=posts)

@app.route('/posts/<int:post_id>/')
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('post/detail.html', post=post)

@app.route('/posts/<int:post_id>/edit/', methods=['GET', 'POST'])
def post_edit(post_id):
    post = Post.query.get(post_id)
    if post is None:
        abort(404)
    if request.method == 'POST':
        post.title=request.form['title']
        post.body=request.form['body']
        post.categories=requiest.form['categories']
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post_id))
    return render_template('post/edit.html', post=post)

@app.route('/posts/<int:post_id>/delete/', methods=['DELETE'])
def post_delete(post_id):
    post = Post.query.get(post_id)
    if post is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(event)
    db.session.commit()
    return jsonify({'status': 'OK'})


from flask import request, redirect, url_for, render_template, flash, abort, jsonify, session
from flaskr import app, db, data
from flaskr.models import Event, Entry, User

#@app.route('/')
#def show_entries():
#    entries = Entry.query.order_by(Entry.id.desc()).all()
#    return render_template('show_entries.html', entries=entries)

#@app.route('/add', methods=['POST'])
#def add_entry():
#    entry = Entry(
#            title=request.form['title'],
#            text=request.form['text']
#            )
#    db.session.add(entry)
#    db.session.commit()
#    flash('New entry was successfully posted')
#    return redirect(url_for('show_entries'))


@app.route('/')
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
        event = Event(title=request.form['title'],
                      description=request.form['description'],
                      day=day,
                      room=room,
                      time=time
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event_list'))
    return render_template('event/edit.html', day=day, room=room, time=time)

@app.route('/events/')
def event_list():
    events = Event.query.all()
    return render_template('event/list.html', events=events)

@app.route('/events/<int:event_id>/')
def event_detail(event_id):
    event = Event.query.get(event_id)
    event_time = str(int(event.time) + 1)
    return render_template('event/detail.html', event=event, event_time=event_time)

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
def user_list():
    users = User.query.all()
    return render_template('user/list.html', users=users)

@app.route('/users/<int:user_id>/')
def user_detail(user_id):
    return 'detail user ' + str(user_id)

@app.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if request.method == 'POST':
        user.name=request.form['name']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    return render_template('user/edit.html', user=user)

@app.route('/users/create/', methods=['GET', 'POST'])
def user_create():
    if request.method == 'POST':
        user = User(name=request.form['name'])
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

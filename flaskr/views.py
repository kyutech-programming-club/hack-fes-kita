from flask import request, redirect, url_for, render_template, flash, abort, jsonify
from flaskr import app, db
from flaskr.read_csv import get_empty_room_num
from flaskr.models import Event, Entry

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




@app.route('/events/create/', methods=['GET', 'POST'])
def event_create():
    if request.method == 'POST':
        event = Event(title=request.form['title'],
                    description=request.form['description'],
                    day=request.form['day'],
                    room=request.form['room'],
                    time=request.form['time'])
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event_list'))
    return render_template('event/edit.html')

@app.route('/events/')
def event_list():
    events = Event.query.all()
    return render_template('event/list.html', events=events)

@app.route('/events/<int:event_id>/')
def event_detail(event_id):
    event = Event.query.get(event_id)
    return render_template('event/detail.html', event=event)

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


@app.route('/calendar')
def calendar():
    data = get_empty_room_num("./occupied_room.csv")
    return render_template('calendar.html', data=data)

from flask import request, redirect, url_for, render_template, flash
from flaskr import app, db
from flaskr.models import Entry

@app.route('/')
def show_entries():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    entry = Entry(
            title=request.form['title'],
            text=request.form['text']
            )
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/calendar')
def calendar():
    data = {"月": [2, 2, 2, 2, 2],
            "火": [3, 6, 7, 9, 12],
            "水": [9, 6, 1, 2, 4],
            "木": [4, 8, 2, 5, 10],
            "金": [1, 5, 4, 2, 3],            
    }
    return render_template('calendar.html', data=data
)

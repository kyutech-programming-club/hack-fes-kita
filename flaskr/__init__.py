from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('flaskr.config')

db = SQLAlchemy(app)


from flaskr.read_csv import RoomData
data = RoomData("./occupied_room.csv")

import flaskr.views
import flaskr.read_csv


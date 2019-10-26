from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.read_csv import RoomData

app = Flask(__name__)
app.config.from_object('flaskr.config')

db = SQLAlchemy(app)
data = RoomData("./occupied_room.csv")

import flaskr.views
import flaskr.read_csv


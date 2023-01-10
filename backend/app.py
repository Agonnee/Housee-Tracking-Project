import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL") or ""
db = SQLAlchemy(app)
CORS(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Event: {self.description}"

    def __init__(self, description) -> None:
        self.description = description

def format_event(event):
    return {
        "description": event.description,
        "id": event.id,
        "created_at": event.created_at
    }


@app.route('/')
def hello():
    return "Hey! This is a House Task Tracking Project in Development"

# create event
@app.route('/events', methods = ['POST'])
def create_event():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

# get all events
@app.route('/events', methods = ['GET'])
def get_events():
    events = Event.query.order_by(Event.created_at.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events':event_list}

# get single events
@app.route('/events/<id>', methods = ['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).one()
    formatted_event = format_event(event)
    return {'event': formatted_event}

# delete single event
@app.route('/events/<id>', methods = ['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return f'Event (id: {id}) deleted!'

# edit single event
@app.route('/events/<id>', methods = ['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description = description, created_at = datetime.utcnow()))
    db.session.commit()
    return {"event": format_event(event.one())}


if __name__ == '__main__':
    app.run()
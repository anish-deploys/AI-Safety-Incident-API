from flask import Flask, request, jsonify
from models import db, Incident
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///incidents.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([i.serialize() for i in incidents]), 200

@app.route('/incidents', methods=['POST'])
def create_incident():
    data = request.get_json()
    if not data or not all(k in data for k in ("title", "description", "severity")):
        return jsonify({'error': 'Missing required fields'}), 400

    if data["severity"] not in ["Low", "Medium", "High"]:
        return jsonify({'error': 'Invalid severity'}), 400

    incident = Incident(
        title=data["title"],
        description=data["description"],
        severity=data["severity"]
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify(incident.serialize()), 201

@app.route('/incidents/<int:id>', methods=['GET'])
def get_incident(id):
    incident = Incident.query.get(id)
    if not incident:
        return jsonify({'error': 'Incident not found'}), 404
    return jsonify(incident.serialize()), 200

@app.route('/incidents/<int:id>', methods=['DELETE'])
def delete_incident(id):
    incident = Incident.query.get(id)
    if not incident:
        return jsonify({'error': 'Incident not found'}), 404
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

# Add serialize method to model
def serialize(self):
    return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "severity": self.severity,
        "reported_at": self.reported_at.isoformat()
    }

Incident.serialize = serialize

if __name__ == '__main__':
    app.run(debug=True)

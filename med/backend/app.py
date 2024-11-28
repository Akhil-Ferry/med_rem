# Placeholder for app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medication.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'

db = SQLAlchemy(app)
mail = Mail(app)

if __name__ == '__main__':
    with app.app_context():  # Create the application context
        db.create_all()  # Create all tables
    app.run(debug=True)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login successful!', 'user_id': user.id})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/add_prescription', methods=['POST'])
def add_prescription():
    data = request.json
    prescription = Prescription(
        user_id=data['user_id'],
        medication_name=data['medication_name'],
        dosage=data['dosage'],
        schedule=data['schedule']
    )
    db.session.add(prescription)
    db.session.commit()
    return jsonify({'message': 'Prescription added successfully!'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

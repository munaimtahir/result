"""
Simple database initialization without pandas dependencies
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from datetime import datetime, date

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Import models after app is configured
class User(db.Model):
    """Admin user model for system access"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Student(db.Model):
    """Student model with authentication credentials"""
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    id_card_number = db.Column(db.String(20), nullable=False, index=True)
    phone_number = db.Column(db.String(15), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Exam(db.Model):
    """Exam/Assessment model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    passing_marks = db.Column(db.Float, nullable=False)
    exam_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Result(db.Model):
    """Individual student result for specific exam"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user if doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@university.edu',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("Admin user created: username='admin', password='admin123'")
        
        # Create sample students
        sample_students = [
            {
                'roll_number': '2023001',
                'id_card_number': 'ID001',
                'phone_number': '+1234567890',
                'name': 'Alice Johnson',
                'email': 'alice@student.edu',
                'year': 1,
                'section': 'A'
            },
            {
                'roll_number': '2023002',
                'id_card_number': 'ID002',
                'phone_number': '+1234567891',
                'name': 'Bob Smith',
                'email': 'bob@student.edu',
                'year': 1,
                'section': 'A'
            },
            {
                'roll_number': '2023003',
                'id_card_number': 'ID003',
                'phone_number': '+1234567892',
                'name': 'Carol Davis',
                'email': 'carol@student.edu',
                'year': 1,
                'section': 'B'
            }
        ]
        
        for student_data in sample_students:
            if not Student.query.filter_by(roll_number=student_data['roll_number']).first():
                student = Student(**student_data)
                db.session.add(student)
        
        # Create sample exams
        sample_exams = [
            {
                'name': 'Mid-term Examination',
                'exam_type': 'mid-term',
                'year': 1,
                'semester': 1,
                'subject': 'Anatomy',
                'total_marks': 100,
                'passing_marks': 50,
                'exam_date': date(2023, 10, 15)
            },
            {
                'name': 'Final Examination',
                'exam_type': 'final',
                'year': 1,
                'semester': 1,
                'subject': 'Physiology',
                'total_marks': 100,
                'passing_marks': 50,
                'exam_date': date(2023, 12, 20)
            }
        ]
        
        for exam_data in sample_exams:
            exam = Exam.query.filter_by(
                name=exam_data['name'],
                subject=exam_data['subject'],
                year=exam_data['year'],
                semester=exam_data['semester']
            ).first()
            
            if not exam:
                exam = Exam(**exam_data)
                db.session.add(exam)
        
        # Commit changes
        db.session.commit()
        
        # Create sample results
        admin = User.query.filter_by(username='admin').first()
        student = Student.query.filter_by(roll_number='2023001').first()
        exam = Exam.query.filter_by(subject='Anatomy').first()
        
        if student and exam and admin:
            existing_result = Result.query.filter_by(student_id=student.id, exam_id=exam.id).first()
            if not existing_result:
                result = Result(
                    student_id=student.id,
                    exam_id=exam.id,
                    marks_obtained=85,
                    grade='A',
                    status='Pass',
                    uploaded_by=admin.id
                )
                db.session.add(result)
        
        db.session.commit()
        print("Sample data initialized successfully!")
        print("\nTest Credentials:")
        print("Student: roll_number='2023001', id_card_number='ID001' or phone='+1234567890'")
        print("Admin: username='admin', password='admin123'")

if __name__ == '__main__':
    init_database()
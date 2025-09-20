"""
Database models for University Result Portal
"""

from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt

class User(UserMixin, db.Model):
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
    
    def __repr__(self):
        return f'<User {self.username}>'

class Student(db.Model):
    """Student model with authentication credentials"""
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    id_card_number = db.Column(db.String(20), nullable=False, index=True)
    phone_number = db.Column(db.String(15), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=False)  # 1-5 for MBBS
    section = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with results
    results = db.relationship('Result', backref='student', lazy='dynamic')
    
    def __repr__(self):
        return f'<Student {self.roll_number} - {self.name}>'

class Exam(db.Model):
    """Exam/Assessment model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # Mid-term, Final, etc.
    year = db.Column(db.Integer, nullable=False)  # Academic year
    semester = db.Column(db.Integer, nullable=False)  # 1-10 for 5-year program
    subject = db.Column(db.String(100), nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    passing_marks = db.Column(db.Float, nullable=False)
    exam_date = db.Column(db.Date, nullable=True)
    result_published_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with results
    results = db.relationship('Result', backref='exam', lazy='dynamic')
    
    def __repr__(self):
        return f'<Exam {self.name} - {self.subject}>'

class Result(db.Model):
    """Individual student result for specific exam"""
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=True)  # A+, A, B+, etc.
    status = db.Column(db.String(20), nullable=False)  # Pass, Fail, Absent
    remarks = db.Column(db.Text, nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Composite unique constraint to prevent duplicate results
    __table_args__ = (db.UniqueConstraint('student_id', 'exam_id', name='_student_exam_uc'),)
    
    @property
    def percentage(self):
        if self.exam.total_marks > 0:
            return (self.marks_obtained / self.exam.total_marks) * 100
        return 0
    
    @property
    def is_pass(self):
        return self.status.lower() == 'pass' and self.marks_obtained >= self.exam.passing_marks
    
    def __repr__(self):
        return f'<Result {self.student.roll_number} - {self.exam.name}: {self.marks_obtained}>'

class ResultUpload(db.Model):
    """Track result upload batches"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_records = db.Column(db.Integer, nullable=False)
    successful_records = db.Column(db.Integer, nullable=False)
    failed_records = db.Column(db.Integer, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Processing')  # Processing, Completed, Failed
    error_log = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<ResultUpload {self.filename} - {self.status}>'
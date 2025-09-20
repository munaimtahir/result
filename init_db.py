"""
Initialize database with sample data for University Result Portal
Run this script to set up initial admin user and sample data
"""

from app import create_app
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Student, Exam, Result
from datetime import datetime, date

# Create app to get access to db
app = create_app()
db = SQLAlchemy()

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
            admin.set_password('admin123')  # Change this in production!
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
            },
            {
                'roll_number': '2022001',
                'id_card_number': 'ID004',
                'phone_number': '+1234567893',
                'name': 'David Wilson',
                'email': 'david@student.edu',
                'year': 2,
                'section': 'A'
            },
            {
                'roll_number': '2022002',
                'id_card_number': 'ID005',
                'phone_number': '+1234567894',
                'name': 'Eva Brown',
                'email': 'eva@student.edu',
                'year': 2,
                'section': 'A'
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
            },
            {
                'name': 'Practical Assessment',
                'exam_type': 'practical',
                'year': 1,
                'semester': 1,
                'subject': 'Biochemistry',
                'total_marks': 50,
                'passing_marks': 25,
                'exam_date': date(2023, 11, 10)
            },
            {
                'name': 'Mid-term Examination',
                'exam_type': 'mid-term',
                'year': 2,
                'semester': 3,
                'subject': 'Pathology',
                'total_marks': 100,
                'passing_marks': 50,
                'exam_date': date(2023, 10, 25)
            }
        ]
        
        created_exams = []
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
                created_exams.append(exam)
            else:
                created_exams.append(exam)
        
        # Commit to get IDs
        db.session.commit()
        
        # Create sample results
        sample_results = [
            # Anatomy results for Year 1 students
            {'student_roll': '2023001', 'exam_subject': 'Anatomy', 'marks': 85, 'grade': 'A', 'status': 'Pass'},
            {'student_roll': '2023002', 'exam_subject': 'Anatomy', 'marks': 72, 'grade': 'B+', 'status': 'Pass'},
            {'student_roll': '2023003', 'exam_subject': 'Anatomy', 'marks': 45, 'grade': 'C', 'status': 'Fail'},
            
            # Physiology results for Year 1 students
            {'student_roll': '2023001', 'exam_subject': 'Physiology', 'marks': 78, 'grade': 'B+', 'status': 'Pass'},
            {'student_roll': '2023002', 'exam_subject': 'Physiology', 'marks': 68, 'grade': 'B', 'status': 'Pass'},
            {'student_roll': '2023003', 'exam_subject': 'Physiology', 'marks': 55, 'grade': 'C+', 'status': 'Pass'},
            
            # Biochemistry practical results
            {'student_roll': '2023001', 'exam_subject': 'Biochemistry', 'marks': 42, 'grade': 'A', 'status': 'Pass'},
            {'student_roll': '2023002', 'exam_subject': 'Biochemistry', 'marks': 38, 'grade': 'B+', 'status': 'Pass'},
            {'student_roll': '2023003', 'exam_subject': 'Biochemistry', 'marks': 20, 'grade': 'F', 'status': 'Fail'},
            
            # Pathology results for Year 2 students
            {'student_roll': '2022001', 'exam_subject': 'Pathology', 'marks': 88, 'grade': 'A', 'status': 'Pass'},
            {'student_roll': '2022002', 'exam_subject': 'Pathology', 'marks': 75, 'grade': 'B+', 'status': 'Pass'},
        ]
        
        for result_data in sample_results:
            # Find student and exam
            student = Student.query.filter_by(roll_number=result_data['student_roll']).first()
            exam = Exam.query.filter_by(subject=result_data['exam_subject']).first()
            
            if student and exam:
                # Check if result already exists
                existing_result = Result.query.filter_by(student_id=student.id, exam_id=exam.id).first()
                if not existing_result:
                    result = Result(
                        student_id=student.id,
                        exam_id=exam.id,
                        marks_obtained=result_data['marks'],
                        grade=result_data['grade'],
                        status=result_data['status'],
                        uploaded_by=admin.id
                    )
                    db.session.add(result)
        
        # Commit all changes
        db.session.commit()
        print("Sample data initialized successfully!")
        print("\nTest Credentials:")
        print("Student: roll_number='2023001', id_card_number='ID001' or phone='+1234567890'")
        print("Admin: username='admin', password='admin123'")

if __name__ == '__main__':
    init_database()
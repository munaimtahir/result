"""
Admin panel routes
"""

import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.admin import bp
from app import db
from app.models import User, Student, Exam, Result, ResultUpload
from app.forms import ExamForm, StudentForm, ResultUploadForm, ManualResultForm

@bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    total_students = Student.query.count()
    total_exams = Exam.query.count()
    total_results = Result.query.count()
    recent_uploads = ResultUpload.query.order_by(ResultUpload.upload_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                         total_students=total_students,
                         total_exams=total_exams,
                         total_results=total_results,
                         recent_uploads=recent_uploads)

@bp.route('/students')
@login_required
def students():
    """List all students"""
    page = request.args.get('page', 1, type=int)
    students = Student.query.order_by(Student.roll_number).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin/students.html', title='Students', students=students)

@bp.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add new student"""
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            roll_number=form.roll_number.data,
            id_card_number=form.id_card_number.data,
            phone_number=form.phone_number.data,
            name=form.name.data,
            email=form.email.data,
            year=form.year.data,
            section=form.section.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('admin.students'))
    
    return render_template('admin/student_form.html', title='Add Student', form=form)

@bp.route('/exams')
@login_required
def exams():
    """List all exams"""
    page = request.args.get('page', 1, type=int)
    exams = Exam.query.order_by(Exam.year.desc(), Exam.semester.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('admin/exams.html', title='Exams', exams=exams)

@bp.route('/exam/add', methods=['GET', 'POST'])
@login_required
def add_exam():
    """Add new exam"""
    form = ExamForm()
    if form.validate_on_submit():
        exam = Exam(
            name=form.name.data,
            exam_type=form.exam_type.data,
            year=form.year.data,
            semester=form.semester.data,
            subject=form.subject.data,
            total_marks=form.total_marks.data,
            passing_marks=form.passing_marks.data,
            exam_date=form.exam_date.data
        )
        db.session.add(exam)
        db.session.commit()
        flash('Exam added successfully!', 'success')
        return redirect(url_for('admin.exams'))
    
    return render_template('admin/exam_form.html', title='Add Exam', form=form)

@bp.route('/upload_results', methods=['GET', 'POST'])
@login_required
def upload_results():
    """Upload results from file"""
    form = ResultUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        exam_id = form.exam_id.data
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the uploaded file
            success_count, error_count, errors = process_result_file(file_path, exam_id, current_user.id)
            
            # Record the upload
            upload_record = ResultUpload(
                filename=filename,
                exam_id=exam_id,
                uploaded_by=current_user.id,
                total_records=success_count + error_count,
                successful_records=success_count,
                failed_records=error_count,
                status='Completed' if error_count == 0 else 'Completed with errors',
                error_log='\n'.join(errors) if errors else None
            )
            db.session.add(upload_record)
            db.session.commit()
            
            flash(f'Results uploaded! {success_count} successful, {error_count} errors.', 
                  'success' if error_count == 0 else 'warning')
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/upload_results.html', title='Upload Results', form=form)

def process_result_file(file_path, exam_id, user_id):
    """Process uploaded result file and return success/error counts"""
    try:
        # Import pandas only when needed to avoid startup issues
        import pandas as pd
        
        # Read file based on extension
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        success_count = 0
        error_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Expected columns: roll_number, marks_obtained, grade, status, remarks
                roll_number = str(row['roll_number']).strip()
                marks_obtained = float(row['marks_obtained'])
                grade = str(row.get('grade', '')).strip()
                status = str(row.get('status', 'Pass')).strip()
                remarks = str(row.get('remarks', '')).strip()
                
                # Find student
                student = Student.query.filter_by(roll_number=roll_number).first()
                if not student:
                    errors.append(f"Row {index + 1}: Student with roll number {roll_number} not found")
                    error_count += 1
                    continue
                
                # Check if result already exists
                existing_result = Result.query.filter_by(student_id=student.id, exam_id=exam_id).first()
                if existing_result:
                    errors.append(f"Row {index + 1}: Result already exists for {roll_number}")
                    error_count += 1
                    continue
                
                # Create new result
                result = Result(
                    student_id=student.id,
                    exam_id=exam_id,
                    marks_obtained=marks_obtained,
                    grade=grade if grade else None,
                    status=status,
                    remarks=remarks if remarks else None,
                    uploaded_by=user_id
                )
                db.session.add(result)
                success_count += 1
                
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")
                error_count += 1
        
        db.session.commit()
        return success_count, error_count, errors
        
    except Exception as e:
        return 0, 1, [f"File processing error: {str(e)}"]
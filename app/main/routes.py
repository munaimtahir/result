"""
Main application routes
"""

from flask import render_template, request, flash
from app.main import bp
from app.forms import StudentLookupForm
from app.models import Student, Result
from sqlalchemy import or_

@bp.route('/')
@bp.route('/index')
def index():
    """Home page with student result lookup"""
    form = StudentLookupForm()
    return render_template('main/index.html', title='University Result Portal', form=form)

@bp.route('/lookup_results', methods=['POST'])
def lookup_results():
    """Look up student results"""
    form = StudentLookupForm()
    
    if form.validate_on_submit():
        roll_number = form.roll_number.data
        id_card_number = form.id_card_number.data
        phone_number = form.phone_number.data
        
        # Build query based on provided authentication
        query = Student.query.filter_by(roll_number=roll_number)
        
        if id_card_number:
            query = query.filter_by(id_card_number=id_card_number)
        elif phone_number:
            query = query.filter_by(phone_number=phone_number)
        
        student = query.first()
        
        if student:
            # Get all results for this student
            results = Result.query.filter_by(student_id=student.id)\
                          .join(Result.exam)\
                          .order_by('exam.year', 'exam.semester', 'exam.name').all()
            
            if results:
                return render_template('main/results.html', 
                                     title=f'Results for {student.name}',
                                     student=student, 
                                     results=results)
            else:
                flash('No results found for this student.', 'info')
        else:
            flash('Invalid credentials. Please check your roll number and verification details.', 'danger')
    
    return render_template('main/index.html', title='University Result Portal', form=form)

@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html', title='About')

@bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('main/contact.html', title='Contact Us')
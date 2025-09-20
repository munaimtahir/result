"""
Results specific routes
"""

from flask import render_template, request
from app.results import bp
from app.models import Result, Exam, Student

@bp.route('/by_exam/<int:exam_id>')
def by_exam(exam_id):
    """View all results for a specific exam"""
    exam = Exam.query.get_or_404(exam_id)
    page = request.args.get('page', 1, type=int)
    
    results = Result.query.filter_by(exam_id=exam_id)\
                    .join(Result.student)\
                    .order_by(Student.roll_number)\
                    .paginate(page=page, per_page=50, error_out=False)
    
    return render_template('results/by_exam.html', 
                         title=f'Results - {exam.name}',
                         exam=exam, 
                         results=results)

@bp.route('/statistics/<int:exam_id>')
def statistics(exam_id):
    """Show statistics for an exam"""
    exam = Exam.query.get_or_404(exam_id)
    results = Result.query.filter_by(exam_id=exam_id).all()
    
    if not results:
        return render_template('results/statistics.html', 
                             title=f'Statistics - {exam.name}',
                             exam=exam, 
                             no_results=True)
    
    # Calculate statistics
    total_students = len(results)
    passed_students = len([r for r in results if r.is_pass])
    failed_students = total_students - passed_students
    
    marks_list = [r.marks_obtained for r in results if r.status != 'Absent']
    
    if marks_list:
        avg_marks = sum(marks_list) / len(marks_list)
        highest_marks = max(marks_list)
        lowest_marks = min(marks_list)
    else:
        avg_marks = highest_marks = lowest_marks = 0
    
    pass_percentage = (passed_students / total_students) * 100 if total_students > 0 else 0
    
    # Grade distribution
    grade_distribution = {}
    for result in results:
        grade = result.grade or 'No Grade'
        grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
    
    stats = {
        'total_students': total_students,
        'passed_students': passed_students,
        'failed_students': failed_students,
        'pass_percentage': round(pass_percentage, 2),
        'avg_marks': round(avg_marks, 2),
        'highest_marks': highest_marks,
        'lowest_marks': lowest_marks,
        'grade_distribution': grade_distribution
    }
    
    return render_template('results/statistics.html', 
                         title=f'Statistics - {exam.name}',
                         exam=exam, 
                         stats=stats)
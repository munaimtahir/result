"""
Forms for University Result Portal
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from app.models import Student, Exam

class LoginForm(FlaskForm):
    """Admin login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentLookupForm(FlaskForm):
    """Student result lookup form with dual authentication"""
    roll_number = StringField('Roll Number', validators=[DataRequired(), Length(min=5, max=20)])
    
    # Authentication option 1: ID Card Number
    id_card_number = StringField('ID Card Number', validators=[Optional(), Length(min=5, max=20)])
    
    # Authentication option 2: Phone Number
    phone_number = StringField('Phone Number', validators=[Optional(), Length(min=10, max=15)])
    
    submit = SubmitField('View Results')
    
    def validate(self, **kwargs):
        """Custom validation to ensure at least one authentication method is provided"""
        if not super().validate(**kwargs):
            return False
            
        if not self.id_card_number.data and not self.phone_number.data:
            self.id_card_number.errors.append('Please provide either ID Card Number or Phone Number')
            self.phone_number.errors.append('Please provide either ID Card Number or Phone Number')
            return False
            
        return True

class ExamForm(FlaskForm):
    """Form for creating/editing exams"""
    name = StringField('Exam Name', validators=[DataRequired(), Length(max=100)])
    exam_type = SelectField('Exam Type', 
                          choices=[('mid-term', 'Mid-term'), ('final', 'Final'), ('sessional', 'Sessional'), ('practical', 'Practical')],
                          validators=[DataRequired()])
    year = IntegerField('Academic Year', validators=[DataRequired(), NumberRange(min=1, max=5)])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=10)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    total_marks = FloatField('Total Marks', validators=[DataRequired(), NumberRange(min=1)])
    passing_marks = FloatField('Passing Marks', validators=[DataRequired(), NumberRange(min=1)])
    exam_date = DateField('Exam Date', validators=[Optional()])
    submit = SubmitField('Save Exam')

class StudentForm(FlaskForm):
    """Form for creating/editing students"""
    roll_number = StringField('Roll Number', validators=[DataRequired(), Length(max=20)])
    id_card_number = StringField('ID Card Number', validators=[DataRequired(), Length(max=20)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    name = StringField('Student Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1, max=5)])
    section = StringField('Section', validators=[Optional(), Length(max=10)])
    submit = SubmitField('Save Student')

class ResultUploadForm(FlaskForm):
    """Form for uploading result files"""
    exam_id = SelectField('Select Exam', coerce=int, validators=[DataRequired()])
    file = FileField('Result File', validators=[
        FileRequired(),
        FileAllowed(['csv', 'xlsx', 'xls'], 'Only CSV and Excel files are allowed!')
    ])
    submit = SubmitField('Upload Results')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exam_id.choices = [(exam.id, f"{exam.name} - {exam.subject} (Year {exam.year}, Sem {exam.semester})") 
                               for exam in Exam.query.order_by(Exam.year.desc(), Exam.semester.desc()).all()]

class ManualResultForm(FlaskForm):
    """Form for manually entering individual results"""
    student_roll = StringField('Student Roll Number', validators=[DataRequired()])
    exam_id = SelectField('Select Exam', coerce=int, validators=[DataRequired()])
    marks_obtained = FloatField('Marks Obtained', validators=[DataRequired(), NumberRange(min=0)])
    grade = SelectField('Grade', 
                       choices=[('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'), 
                               ('C+', 'C+'), ('C', 'C'), ('D', 'D'), ('F', 'F')],
                       validators=[Optional()])
    status = SelectField('Status',
                        choices=[('Pass', 'Pass'), ('Fail', 'Fail'), ('Absent', 'Absent')],
                        validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Save Result')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exam_id.choices = [(exam.id, f"{exam.name} - {exam.subject}") 
                               for exam in Exam.query.order_by(Exam.created_at.desc()).all()]
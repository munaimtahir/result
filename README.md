# University Result Portal

A comprehensive web-based result management system for MBBS program, built with Python Flask.

## Features

### For Students
- **Secure Result Access**: Dual authentication using roll number + ID card number OR roll number + phone number
- **Real-time Results**: Instant access to published examination results
- **Comprehensive View**: View all results across semesters with statistics
- **Mobile Responsive**: Access from any device

### For Administrators
- **Dashboard**: Overview of students, exams, and results
- **Student Management**: Add and manage student records
- **Exam Management**: Create and organize examinations
- **Bulk Result Upload**: Upload results via CSV/Excel files
- **Result Analytics**: View statistics and performance metrics

## System Requirements

- Python 3.7+
- Flask 2.3+
- SQLite (default) or PostgreSQL/MySQL
- Modern web browser

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/munaimtahir/result.git
   cd result
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open http://localhost:5000 in your browser
   - Admin login: username=`admin`, password=`admin123`
   - Test student: roll=`2023001`, id=`ID001` or phone=`+1234567890`

## Directory Structure

```
result/
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── forms.py           # WTForms definitions
│   ├── auth/              # Authentication routes
│   ├── main/              # Main public routes
│   ├── admin/             # Admin panel routes
│   ├── results/           # Result-specific routes
│   ├── static/            # CSS, JS, images
│   └── templates/         # HTML templates
├── uploads/               # File upload directory
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
└── README.md
```

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `MAIL_SERVER`: Email server for notifications
- `UPLOAD_FOLDER`: Directory for uploaded files

### Database Configuration
The system uses SQLite by default. For production, configure PostgreSQL or MySQL in `config.py`.

## Usage Guide

### Student Access
1. Visit the homepage
2. Enter roll number
3. Provide either ID card number OR phone number
4. View results with statistics

### Admin Operations

#### Adding Students
1. Login to admin panel
2. Navigate to Students → Add Student
3. Fill in student details
4. Save student record

#### Creating Exams
1. Go to Exams → Add Exam
2. Configure exam details (subject, marks, dates)
3. Save exam

#### Uploading Results
1. Navigate to Upload Results
2. Select target exam
3. Upload CSV/Excel file with required format:
   ```csv
   roll_number,marks_obtained,grade,status,remarks
   2023001,85,A,Pass,Excellent
   2023002,72,B+,Pass,Good
   ```

## File Upload Format

### Required Columns
- **roll_number**: Student's roll number (must exist in system)
- **marks_obtained**: Numerical marks scored

### Optional Columns
- **grade**: Letter grade (A+, A, B+, B, C+, C, D, F)
- **status**: Pass/Fail/Absent (defaults to Pass)
- **remarks**: Additional comments

### Supported Formats
- CSV (.csv)
- Excel (.xlsx, .xls)
- Maximum file size: 16MB

## Security Features

- Password hashing with bcrypt
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Input validation and sanitization
- Dual authentication for student access
- Role-based admin access

## Academic Structure

The system supports:
- **5-year MBBS program**
- **10 semesters** (2 per year)
- **Multiple exam types**: Mid-term, Final, Sessional, Practical
- **Grade system**: A+ to F with pass/fail status
- **Performance analytics**: Pass rates, averages, distributions

## API Endpoints

### Public Endpoints
- `GET /` - Homepage with student lookup
- `POST /lookup_results` - Student result lookup
- `GET /about` - About page
- `GET /contact` - Contact information

### Admin Endpoints (Login Required)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/students` - Student management
- `GET /admin/exams` - Exam management
- `POST /admin/upload_results` - Result upload

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Database Migrations
For schema changes, use Flask-Migrate:
```bash
pip install Flask-Migrate
flask db init
flask db migrate -m "Description"
flask db upgrade
```

## Deployment

### Production Setup
1. Set environment variables:
   ```bash
   export SECRET_KEY="your-production-secret-key"
   export DATABASE_URL="postgresql://user:pass@localhost/resultdb"
   ```

2. Use production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

3. Configure reverse proxy (nginx/Apache)
4. Set up SSL certificate
5. Configure database backups

## Troubleshooting

### Common Issues

1. **Database not found**
   ```bash
   python init_db.py
   ```

2. **File upload errors**
   - Check file format (CSV/Excel)
   - Verify file size < 16MB
   - Ensure required columns exist

3. **Student login issues**
   - Verify roll number format
   - Check ID card/phone number matches
   - Ensure student exists in system

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Support

For technical support or questions:
- Email: support@university.edu
- Phone: +1 (555) 123-4568
- Create an issue on GitHub

## Changelog

### Version 1.0.0
- Initial release
- Student result lookup with dual authentication
- Admin panel for result management
- Bulk result upload via CSV/Excel
- Responsive web interface
- Performance analytics and statistics
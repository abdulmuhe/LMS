# Professional Learning Management System (LMS)

A comprehensive, role-based Learning Management System built with Django, featuring modern UI/UX and advanced analytics.

## 🚀 Features

### Role-Based Dashboards
- **Common Institutional Dashboard**: Overview visible to all users
- **Student Dashboard**: Personal progress, enrolled courses, assignments
- **Professor Dashboard**: Course management, grading, student analytics
- **Admin Dashboard**: Complete system control and user management
- **Manager Dashboard**: High-level analytics and performance insights

### Core Functionality
- **User Management**: Multi-role authentication system
- **Course Management**: Complete course lifecycle management
- **Assignment System**: Create, submit, and grade assignments
- **Progress Tracking**: Real-time progress monitoring
- **Analytics**: Comprehensive reporting and insights
- **Certificate Generation**: Automatic certificate issuance
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Authentication**: Django's built-in auth system

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation & Setup

### 1. Clone the Repository
\`\`\`bash
git clone <repository-url>
cd django-lms-professional
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
python -m venv lms_env
source lms_env/bin/activate  # On Windows: lms_env\Scripts\activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Settings
\`\`\`bash
# Copy settings template (if needed)
cp lms_project/settings.py.example lms_project/settings.py
\`\`\`

### 5. Database Setup
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 6. Create Sample Data
\`\`\`bash
python scripts/create_sample_data.py
\`\`\`

### 7. Run Development Server
\`\`\`bash
python manage.py runserver
\`\`\`

Visit `http://127.0.0.1:8000` to access the LMS.

## 👥 Demo Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `password123`

### Manager Access
- **Username**: `manager1`
- **Password**: `password123`

### Professor Access
- **Username**: `prof_smith`
- **Password**: `password123`

### Student Access
- **Username**: `student1`
- **Password**: `password123`

## 📊 System Architecture

### Models Overview
- **User**: Extended user model with role-based permissions
- **Department**: Academic departments
- **Course**: Course information and management
- **Enrollment**: Student-course relationships
- **Assignment**: Assignment creation and management
- **Submission**: Student assignment submissions
- **Announcement**: System and course announcements
- **Certificate**: Auto-generated completion certificates

### Role Permissions
- **Students**: Enroll in courses, submit assignments, view progress
- **Professors**: Manage courses, create assignments, grade submissions
- **Admins**: Full system access, user management, system configuration
- **Managers**: Analytics access, performance monitoring, reporting

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on all device sizes
- **Interactive Charts**: Real-time data visualization
- **Intuitive Navigation**: Role-based sidebar navigation
- **Progress Indicators**: Visual progress tracking
- **Status Badges**: Clear status indicators
- **Hover Effects**: Enhanced user interaction

## 📈 Analytics & Reporting

### Student Analytics
- Course progress tracking
- Grade performance
- Assignment completion rates
- Learning path visualization

### Professor Analytics
- Class performance overview
- Assignment submission tracking
- Student engagement metrics
- Grading efficiency tools

### Admin Analytics
- System-wide statistics
- User activity monitoring
- Course performance metrics
- Department comparisons

### Manager Analytics
- High-level KPIs
- Trend analysis
- Performance benchmarking
- Strategic insights

## 🔒 Security Features

- **Role-based Access Control**: Strict permission system
- **CSRF Protection**: Built-in Django security
- **SQL Injection Prevention**: ORM-based queries
- **XSS Protection**: Template auto-escaping
- **Secure File Uploads**: Validated file handling

## 🚀 Production Deployment

### Environment Variables
\`\`\`bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com
\`\`\`

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lms_production',
        'USER': 'lms_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

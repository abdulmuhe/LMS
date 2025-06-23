from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from .models import *
from .forms import *

def is_student(user):
    return user.role == 'student'

def is_professor(user):
    return user.role == 'professor'

def is_admin(user):
    return user.role == 'admin'

def is_manager(user):
    return user.role == 'manager'

def home(request):
    """Common institutional dashboard visible to all users"""
    if not request.user.is_authenticated:
        return redirect('lms:login')
    
    # Common statistics
    total_students = User.objects.filter(role='student', is_active=True).count()
    total_professors = User.objects.filter(role='professor', is_active=True).count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.filter(is_active=True).count()
    
    # Course completion rates
    courses_with_completion = []
    for course in Course.objects.filter(is_active=True)[:5]:
        courses_with_completion.append({
            'name': course.title,
            'completion_rate': course.completion_rate,
            'enrolled_count': course.enrolled_students_count
        })
    
    # Recent announcements
    recent_announcements = Announcement.objects.filter(
        is_active=True, is_global=True
    ).order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_professors': total_professors,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'courses_with_completion': courses_with_completion,
        'recent_announcements': recent_announcements,
    }
    
    return render(request, 'lms/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('lms:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('lms:dashboard')
            else:
                messages.error(request, 'Invalid credentials or inactive account.')
    else:
        form = LoginForm()
    
    return render(request, 'lms/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('lms:dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('lms:login')
    else:
        form = RegistrationForm()
    
    return render(request, 'lms/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('lms:login')

@login_required
def dashboard(request):
    """Role-based dashboard redirection"""
    if request.user.role == 'student':
        return redirect('lms:student_dashboard')
    elif request.user.role == 'professor':
        return redirect('lms:professor_dashboard')
    elif request.user.role == 'admin':
        return redirect('lms:admin_dashboard')
    elif request.user.role == 'manager':
        return redirect('lms:manager_dashboard')
    else:
        return redirect('lms:home')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    """Student personalized dashboard"""
    student = request.user
    
    # Enrolled courses
    enrollments = Enrollment.objects.filter(
        student=student, is_active=True
    ).select_related('course')
    
    # Pending assignments
    pending_assignments = []
    for enrollment in enrollments:
        assignments = Assignment.objects.filter(
            course=enrollment.course, 
            is_active=True,
            due_date__gte=timezone.now()
        ).exclude(
            submission__student=student
        )
        for assignment in assignments:
            pending_assignments.append({
                'assignment': assignment,
                'course': enrollment.course,
                'days_left': (assignment.due_date.date() - timezone.now().date()).days
            })
    
    # Recent grades
    recent_submissions = Submission.objects.filter(
        student=student, status='graded'
    ).select_related('assignment', 'assignment__course').order_by('-graded_at')[:5]
    
    # Overall progress
    total_courses = enrollments.count()
    completed_courses = enrollments.filter(progress=100).count()
    overall_progress = (completed_courses / total_courses * 100) if total_courses > 0 else 0
    
    context = {
        'enrollments': enrollments,
        'pending_assignments': pending_assignments[:5],
        'recent_submissions': recent_submissions,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'overall_progress': round(overall_progress, 2),
    }
    
    return render(request, 'lms/student_dashboard.html', context)

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    """Professor personalized dashboard"""
    professor = request.user
    
    # Courses taught
    courses = Course.objects.filter(instructor=professor, is_active=True)
    
    # Recent submissions to grade
    pending_submissions = Submission.objects.filter(
        assignment__course__instructor=professor,
        status='submitted'
    ).select_related('assignment', 'student', 'assignment__course').order_by('-submitted_at')[:10]
    
    # Course statistics
    course_stats = []
    for course in courses:
        stats = {
            'course': course,
            'enrolled_students': course.enrolled_students_count,
            'completion_rate': course.completion_rate,
            'assignments_count': Assignment.objects.filter(course=course, is_active=True).count(),
            'pending_submissions': Submission.objects.filter(
                assignment__course=course, status='submitted'
            ).count()
        }
        course_stats.append(stats)
    
    context = {
        'courses': courses,
        'pending_submissions': pending_submissions,
        'course_stats': course_stats,
    }
    
    return render(request, 'lms/professor_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin control panel dashboard"""
    # User statistics
    user_stats = {
        'total_users': User.objects.filter(is_active=True).count(),
        'students': User.objects.filter(role='student', is_active=True).count(),
        'professors': User.objects.filter(role='professor', is_active=True).count(),
        'admins': User.objects.filter(role='admin', is_active=True).count(),
        'managers': User.objects.filter(role='manager', is_active=True).count(),
    }
    
    # Course statistics
    course_stats = {
        'total_courses': Course.objects.filter(is_active=True).count(),
        'active_enrollments': Enrollment.objects.filter(is_active=True).count(),
        'completed_courses': Enrollment.objects.filter(progress=100).count(),
        'total_assignments': Assignment.objects.filter(is_active=True).count(),
    }
    
    # Recent activities
    recent_users = User.objects.filter(is_active=True).order_by('-date_joined')[:5]
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:5]
    recent_enrollments = Enrollment.objects.filter(is_active=True).order_by('-enrollment_date')[:5]
    
    # Performance metrics
    departments = Department.objects.all()
    department_stats = []
    for dept in departments:
        dept_courses = Course.objects.filter(department=dept, is_active=True)
        total_enrollments = Enrollment.objects.filter(course__in=dept_courses, is_active=True).count()
        completed_enrollments = Enrollment.objects.filter(course__in=dept_courses, progress=100).count()
        completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0
        
        department_stats.append({
            'department': dept.name,
            'courses': dept_courses.count(),
            'enrollments': total_enrollments,
            'completion_rate': round(completion_rate, 2)
        })
    
    context = {
        'user_stats': user_stats,
        'course_stats': course_stats,
        'recent_users': recent_users,
        'recent_courses': recent_courses,
        'recent_enrollments': recent_enrollments,
        'department_stats': department_stats,
    }
    
    return render(request, 'lms/admin_dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    """Manager high-level analytics dashboard"""
    # Performance analytics
    total_students = User.objects.filter(role='student', is_active=True).count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.filter(is_active=True).count()
    
    # Completion rates by department
    departments = Department.objects.all()
    department_performance = []
    for dept in departments:
        dept_courses = Course.objects.filter(department=dept, is_active=True)
        enrollments = Enrollment.objects.filter(course__in=dept_courses, is_active=True)
        completed = enrollments.filter(progress=100).count()
        total = enrollments.count()
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        department_performance.append({
            'name': dept.name,
            'completion_rate': round(completion_rate, 2),
            'total_students': total,
            'completed_students': completed
        })
    
    # Monthly enrollment trends (last 6 months)
    enrollment_trends = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        enrollments = Enrollment.objects.filter(
            enrollment_date__range=[month_start, month_end]
        ).count()
        enrollment_trends.append({
            'month': month_start.strftime('%B %Y'),
            'enrollments': enrollments
        })
    
    enrollment_trends.reverse()
    
    # Top performing courses
    top_courses = []
    for course in Course.objects.filter(is_active=True):
        if course.enrolled_students_count > 0:
            top_courses.append({
                'course': course,
                'completion_rate': course.completion_rate,
                'enrolled_count': course.enrolled_students_count
            })
    
    top_courses.sort(key=lambda x: x['completion_rate'], reverse=True)
    top_courses = top_courses[:5]
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'department_performance': department_performance,
        'enrollment_trends': enrollment_trends,
        'top_courses': top_courses,
    }
    
    return render(request, 'lms/manager_dashboard.html', context)

@login_required
def courses_list(request):
    """List all available courses"""
    courses = Course.objects.filter(is_active=True).select_related('instructor', 'department')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        courses = courses.filter(department__name=department_filter)
    
    # Pagination
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    departments = Department.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'departments': departments,
        'department_filter': department_filter,
    }
    
    return render(request, 'lms/courses_list.html', context)

@login_required
def course_detail(request, course_id):
    """Course detail view"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if user is enrolled
    is_enrolled = False
    enrollment = None
    if request.user.role == 'student':
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course, is_active=True)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass
    
    # Get course assignments
    assignments = Assignment.objects.filter(course=course, is_active=True).order_by('due_date')
    
    # Get course announcements
    announcements = Announcement.objects.filter(
        course=course, is_active=True
    ).order_by('-created_at')[:5]
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'assignments': assignments,
        'announcements': announcements,
    }
    
    return render(request, 'lms/course_detail.html', context)

@login_required
def enroll_course(request, course_id):
    """Enroll student in a course"""
    if request.user.role != 'student':
        messages.error(request, 'Only students can enroll in courses.')
        return redirect('lms:courses_list')
    
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('lms:course_detail', course_id=course_id)
    
    # Check if course is full
    if course.enrolled_students_count >= course.max_students:
        messages.error(request, 'This course is full.')
        return redirect('lms:course_detail', course_id=course_id)
    
    # Create enrollment
    Enrollment.objects.create(student=request.user, course=course)
    messages.success(request, f'Successfully enrolled in {course.title}!')
    
    return redirect('lms:course_detail', course_id=course_id)

@login_required
@user_passes_test(is_professor)
def create_assignment(request):
    """Create new assignment"""
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, f'Assignment "{assignment.title}" created successfully!')
            return redirect('lms:professor_dashboard')
    else:
        form = AssignmentForm(user=request.user)
    
    return render(request, 'lms/create_assignment.html', {'form': form})

@login_required
@user_passes_test(is_student)
def submit_assignment(request, assignment_id):
    """Submit assignment"""
    assignment = get_object_or_404(Assignment, id=assignment_id, is_active=True)
    
    # Check if student is enrolled in the course
    if not Enrollment.objects.filter(
        student=request.user, course=assignment.course, is_active=True
    ).exists():
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('lms:courses_list')
    
    # Check if already submitted
    existing_submission = Submission.objects.filter(
        assignment=assignment, student=request.user
    ).first()
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=existing_submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            
            action = 'updated' if existing_submission else 'submitted'
            messages.success(request, f'Assignment {action} successfully!')
            return redirect('lms:course_detail', course_id=assignment.course.id)
    else:
        form = SubmissionForm(instance=existing_submission)
    
    context = {
        'form': form,
        'assignment': assignment,
        'existing_submission': existing_submission,
    }
    
    return render(request, 'lms/submit_assignment.html', context)

@login_required
@user_passes_test(is_professor)
def grade_submission(request, submission_id):
    """Grade student submission"""
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Check if professor teaches this course
    if submission.assignment.course.instructor != request.user:
        messages.error(request, 'You can only grade submissions for your courses.')
        return redirect('lms:professor_dashboard')
    
    if request.method == 'POST':
        form = GradingForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.graded_by = request.user
            submission.graded_at = timezone.now()
            submission.status = 'graded'
            submission.save()
            
            messages.success(request, 'Submission graded successfully!')
            return redirect('lms:professor_dashboard')
    else:
        form = GradingForm(instance=submission)
    
    context = {
        'form': form,
        'submission': submission,
    }
    
    return render(request, 'lms/grade_submission.html', context)

@login_required
@user_passes_test(is_professor)
def view_submissions(request, assignment_id):
    """View all submissions for an assignment"""
    assignment = get_object_or_404(Assignment, id=assignment_id, is_active=True)
    
    # Check if professor teaches this course
    if assignment.course.instructor != request.user:
        messages.error(request, 'You can only view submissions for your courses.')
        return redirect('lms:professor_dashboard')
    
    # Get all submissions for this assignment
    submissions = Submission.objects.filter(assignment=assignment).select_related('student').order_by('-submitted_at')
    
    # Get enrolled students who haven't submitted
    enrolled_students = Enrollment.objects.filter(course=assignment.course, is_active=True).values_list('student', flat=True)
    submitted_students = submissions.values_list('student', flat=True)
    missing_students = User.objects.filter(id__in=enrolled_students).exclude(id__in=submitted_students)
    
    context = {
        'assignment': assignment,
        'submissions': submissions,
        'missing_students': missing_students,
        'total_enrolled': len(enrolled_students),
        'total_submitted': submissions.count(),
    }
    
    return render(request, 'lms/view_submissions.html', context)

@login_required
def analytics_api(request):
    """API endpoint for dashboard analytics"""
    if request.user.role not in ['admin', 'manager']:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Department completion rates
    departments = Department.objects.all()
    department_data = []
    for dept in departments:
        dept_courses = Course.objects.filter(department=dept, is_active=True)
        enrollments = Enrollment.objects.filter(course__in=dept_courses, is_active=True)
        completed = enrollments.filter(progress=100).count()
        total = enrollments.count()
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        department_data.append({
            'name': dept.name,
            'completion_rate': round(completion_rate, 2)
        })
    
    # Monthly enrollment trends
    enrollment_data = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        enrollments = Enrollment.objects.filter(
            enrollment_date__range=[month_start, month_end]
        ).count()
        enrollment_data.append({
            'month': month_start.strftime('%b %Y'),
            'enrollments': enrollments
        })
    
    enrollment_data.reverse()
    
    return JsonResponse({
        'department_completion': department_data,
        'enrollment_trends': enrollment_data
    })

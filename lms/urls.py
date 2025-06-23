from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard routing
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('professor-dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    
    # Course management
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<uuid:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<uuid:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    
    # Assignment management
    path('assignments/create/', views.create_assignment, name='create_assignment'),
    path('assignments/<uuid:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('assignments/<uuid:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),
    path('submissions/<uuid:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    
    # API endpoints
    path('api/analytics/', views.analytics_api, name='analytics_api'),
]

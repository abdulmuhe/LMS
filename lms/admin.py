from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('LMS Info', {
            'fields': ('role', 'profile_picture', 'phone_number', 'date_of_birth', 
                      'address', 'department', 'student_id', 'employee_id')
        }),
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'instructor', 'department', 'credits', 'is_active', 'start_date')
    list_filter = ('department', 'difficulty_level', 'is_active', 'created_at')
    search_fields = ('title', 'code', 'description')
    date_hierarchy = 'start_date'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress', 'grade', 'enrollment_date', 'is_active')
    list_filter = ('is_active', 'enrollment_date', 'course__department')
    search_fields = ('student__username', 'course__title', 'course__code')
    date_hierarchy = 'enrollment_date'

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assignment_type', 'max_points', 'due_date', 'is_active')
    list_filter = ('assignment_type', 'is_active', 'course__department', 'due_date')
    search_fields = ('title', 'description', 'course__title')
    date_hierarchy = 'due_date'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'points_earned', 'submitted_at', 'graded_by')
    list_filter = ('status', 'submitted_at', 'assignment__course__department')
    search_fields = ('student__username', 'assignment__title')
    date_hierarchy = 'submitted_at'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'course', 'is_global', 'is_active', 'created_at')
    list_filter = ('is_global', 'is_active', 'created_at', 'course__department')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'certificate_id', 'grade', 'issued_date')
    list_filter = ('issued_date', 'course__department')
    search_fields = ('student__username', 'course__title', 'certificate_id')
    date_hierarchy = 'issued_date'

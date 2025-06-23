import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from lms.models import User, Department, Course, Enrollment, Assignment, Submission, Announcement

def create_sample_data():
    print("Creating sample data for LMS...")
    
    # Create Departments
    departments = [
        {'name': 'Computer Science', 'description': 'Department of Computer Science and Engineering'},
        {'name': 'Mathematics', 'description': 'Department of Mathematics'},
        {'name': 'Physics', 'description': 'Department of Physics'},
        {'name': 'Business', 'description': 'School of Business Administration'},
        {'name': 'Literature', 'description': 'Department of English Literature'},
    ]
    
    dept_objects = []
    for dept_data in departments:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
        dept_objects.append(dept)
        if created:
            print(f"Created department: {dept.name}")
    
    # Create Admin User
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@lms.edu',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'employee_id': 'ADMIN001'
        }
    )
    if created:
        admin_user.set_password('password123')
        admin_user.save()
        print("Created admin user: admin / password123")
    
    # Create Manager User
    manager_user, created = User.objects.get_or_create(
        username='manager1',
        defaults={
            'email': 'manager@lms.edu',
            'first_name': 'John',
            'last_name': 'Manager',
            'role': 'manager',
            'department_name': 'Administration',  # Changed from department to department_name
            'employee_id': 'MGR001'
        }
    )
    if created:
        manager_user.set_password('password123')
        manager_user.save()
        print("Created manager user: manager1 / password123")
    
    # Create Professor Users
    professors_data = [
        {'username': 'prof_smith', 'first_name': 'Dr. Sarah', 'last_name': 'Smith', 'email': 'sarah.smith@lms.edu', 'department_name': 'Computer Science'},
        {'username': 'prof_johnson', 'first_name': 'Dr. Michael', 'last_name': 'Johnson', 'email': 'michael.johnson@lms.edu', 'department_name': 'Mathematics'},
        {'username': 'prof_williams', 'first_name': 'Dr. Emily', 'last_name': 'Williams', 'email': 'emily.williams@lms.edu', 'department_name': 'Physics'},
        {'username': 'prof_brown', 'first_name': 'Dr. David', 'last_name': 'Brown', 'email': 'david.brown@lms.edu', 'department_name': 'Business'},
        {'username': 'prof_davis', 'first_name': 'Dr. Lisa', 'last_name': 'Davis', 'email': 'lisa.davis@lms.edu', 'department_name': 'Literature'},
    ]
    
    professor_objects = []
    for prof_data in professors_data:
        prof, created = User.objects.get_or_create(
            username=prof_data['username'],
            defaults={
                'email': prof_data['email'],
                'first_name': prof_data['first_name'],
                'last_name': prof_data['last_name'],
                'role': 'professor',
                'department_name': prof_data['department_name'],  # Changed from department to department_name
                'employee_id': f"PROF{prof_data['username'][-3:].upper()}"
            }
        )
        if created:
            prof.set_password('password123')
            prof.save()
            print(f"Created professor: {prof.username} / password123")
        professor_objects.append(prof)
    
    # Create Student Users
    students_data = [
        {'username': 'student1', 'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice.johnson@student.lms.edu'},
        {'username': 'student2', 'first_name': 'Bob', 'last_name': 'Wilson', 'email': 'bob.wilson@student.lms.edu'},
        {'username': 'student3', 'first_name': 'Carol', 'last_name': 'Davis', 'email': 'carol.davis@student.lms.edu'},
        {'username': 'student4', 'first_name': 'David', 'last_name': 'Miller', 'email': 'david.miller@student.lms.edu'},
        {'username': 'student5', 'first_name': 'Eva', 'last_name': 'Garcia', 'email': 'eva.garcia@student.lms.edu'},
        {'username': 'student6', 'first_name': 'Frank', 'last_name': 'Martinez', 'email': 'frank.martinez@student.lms.edu'},
        {'username': 'student7', 'first_name': 'Grace', 'last_name': 'Anderson', 'email': 'grace.anderson@student.lms.edu'},
        {'username': 'student8', 'first_name': 'Henry', 'last_name': 'Taylor', 'email': 'henry.taylor@student.lms.edu'},
        {'username': 'student9', 'first_name': 'Ivy', 'last_name': 'Thomas', 'email': 'ivy.thomas@student.lms.edu'},
        {'username': 'student10', 'first_name': 'Jack', 'last_name': 'White', 'email': 'jack.white@student.lms.edu'},
    ]
    
    student_objects = []
    for student_data in students_data:
        student, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'email': student_data['email'],
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name'],
                'role': 'student',
                'student_id': f"STU{student_data['username'][-1:].upper()}001"
            }
        )
        if created:
            student.set_password('password123')
            student.save()
            print(f"Created student: {student.username} / password123")
        student_objects.append(student)
    
    # Create Courses
    courses_data = [
        {
            'title': 'Introduction to Python Programming',
            'code': 'CS101',
            'description': 'Learn the fundamentals of Python programming including variables, functions, loops, and object-oriented programming.',
            'instructor': professor_objects[0],  # Prof Smith
            'department': dept_objects[0],  # Computer Science
            'credits': 3,
            'difficulty_level': 'beginner',
            'duration_weeks': 12,
            'max_students': 30,
        },
        {
            'title': 'Data Structures and Algorithms',
            'code': 'CS201',
            'description': 'Advanced course covering data structures, algorithms, and their analysis.',
            'instructor': professor_objects[0],  # Prof Smith
            'department': dept_objects[0],  # Computer Science
            'credits': 4,
            'difficulty_level': 'intermediate',
            'duration_weeks': 16,
            'max_students': 25,
        },
        {
            'title': 'Calculus I',
            'code': 'MATH101',
            'description': 'Introduction to differential and integral calculus.',
            'instructor': professor_objects[1],  # Prof Johnson
            'department': dept_objects[1],  # Mathematics
            'credits': 4,
            'difficulty_level': 'intermediate',
            'duration_weeks': 16,
            'max_students': 35,
        },
        {
            'title': 'Physics Fundamentals',
            'code': 'PHYS101',
            'description': 'Basic principles of physics including mechanics, thermodynamics, and waves.',
            'instructor': professor_objects[2],  # Prof Williams
            'department': dept_objects[2],  # Physics
            'credits': 3,
            'difficulty_level': 'beginner',
            'duration_weeks': 14,
            'max_students': 28,
        },
        {
            'title': 'Business Management',
            'code': 'BUS101',
            'description': 'Introduction to business management principles and practices.',
            'instructor': professor_objects[3],  # Prof Brown
            'department': dept_objects[3],  # Business
            'credits': 3,
            'difficulty_level': 'beginner',
            'duration_weeks': 12,
            'max_students': 40,
        },
        {
            'title': 'English Literature Survey',
            'code': 'LIT101',
            'description': 'Survey of major works in English literature from different periods.',
            'instructor': professor_objects[4],  # Prof Davis
            'department': dept_objects[4],  # Literature
            'credits': 3,
            'difficulty_level': 'intermediate',
            'duration_weeks': 14,
            'max_students': 25,
        },
    ]
    
    course_objects = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            code=course_data['code'],
            defaults={
                'title': course_data['title'],
                'description': course_data['description'],
                'instructor': course_data['instructor'],
                'department': course_data['department'],
                'credits': course_data['credits'],
                'difficulty_level': course_data['difficulty_level'],
                'duration_weeks': course_data['duration_weeks'],
                'max_students': course_data['max_students'],
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + timedelta(weeks=course_data['duration_weeks']),
            }
        )
        if created:
            print(f"Created course: {course.code} - {course.title}")
        course_objects.append(course)
    
    # Create Enrollments
    import random
    for student in student_objects:
        # Each student enrolls in 2-4 random courses
        num_courses = random.randint(2, 4)
        selected_courses = random.sample(course_objects, num_courses)
        
        for course in selected_courses:
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                course=course,
                defaults={
                    'progress': random.randint(0, 100),
                    'enrollment_date': timezone.now() - timedelta(days=random.randint(1, 60))
                }
            )
            if created and enrollment.progress == 100:
                # Assign grade for completed courses
                grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
                enrollment.grade = random.choice(grades)
                enrollment.completed_at = timezone.now() - timedelta(days=random.randint(1, 30))
                enrollment.save()
    
    print(f"Created enrollments for {len(student_objects)} students")
    
    # Create Assignments
    assignment_types = ['quiz', 'project', 'essay', 'presentation', 'lab']
    for course in course_objects:
        # Each course has 3-5 assignments
        num_assignments = random.randint(3, 5)
        for i in range(num_assignments):
            assignment, created = Assignment.objects.get_or_create(
                title=f"{course.code} Assignment {i+1}",
                course=course,
                defaults={
                    'description': f"Assignment {i+1} for {course.title}. Complete the required tasks and submit your work.",
                    'assignment_type': random.choice(assignment_types),
                    'max_points': random.choice([50, 75, 100, 150]),
                    'due_date': timezone.now() + timedelta(days=random.randint(7, 30)),
                }
            )
            if created:
                print(f"Created assignment: {assignment.title}")
    
    # Create some sample submissions
    assignments = Assignment.objects.all()
    for assignment in assignments[:10]:  # Only for first 10 assignments
        enrolled_students = Enrollment.objects.filter(course=assignment.course).values_list('student', flat=True)
        # Random subset of students submit
        submitting_students = random.sample(list(enrolled_students), min(len(enrolled_students), random.randint(1, 5)))
        
        for student_id in submitting_students:
            student = User.objects.get(id=student_id)
            submission, created = Submission.objects.get_or_create(
                assignment=assignment,
                student=student,
                defaults={
                    'submission_text': f"This is the submission for {assignment.title} by {student.first_name} {student.last_name}.",
                    'submitted_at': timezone.now() - timedelta(days=random.randint(1, 10)),
                    'points_earned': random.randint(int(assignment.max_points * 0.6), assignment.max_points),
                    'status': random.choice(['submitted', 'graded']),
                    'feedback': "Good work! Keep it up." if random.choice([True, False]) else "",
                }
            )
            if created and submission.status == 'graded':
                submission.graded_by = assignment.course.instructor
                submission.graded_at = timezone.now() - timedelta(days=random.randint(1, 5))
                submission.save()
    
    print("Created sample submissions")
    
    # Create Announcements
    announcements_data = [
        {
            'title': 'Welcome to the New Semester!',
            'content': 'Welcome everyone to the new academic semester. We have exciting courses and opportunities ahead.',
            'author': admin_user,
            'is_global': True,
        },
        {
            'title': 'Library Hours Extended',
            'content': 'The library will now be open until 10 PM on weekdays to support your studies.',
            'author': admin_user,
            'is_global': True,
        },
    ]
    
    for ann_data in announcements_data:
        announcement, created = Announcement.objects.get_or_create(
            title=ann_data['title'],
            defaults={
                'content': ann_data['content'],
                'author': ann_data['author'],
                'is_global': ann_data['is_global'],
            }
        )
        if created:
            print(f"Created announcement: {announcement.title}")
    
    # Create course-specific announcements
    for course in course_objects[:3]:  # First 3 courses
        announcement, created = Announcement.objects.get_or_create(
            title=f"Welcome to {course.title}",
            course=course,
            defaults={
                'content': f"Welcome to {course.title}! Please review the syllabus and prepare for our first class.",
                'author': course.instructor,
                'is_global': False,
            }
        )
        if created:
            print(f"Created course announcement: {announcement.title}")
    
    print("\n" + "="*50)
    print("SAMPLE DATA CREATION COMPLETE!")
    print("="*50)
    print("\nLogin Credentials:")
    print("Admin: admin / password123")
    print("Manager: manager1 / password123")
    print("Professors: prof_smith, prof_johnson, prof_williams, prof_brown, prof_davis / password123")
    print("Students: student1, student2, ..., student10 / password123")
    print("\nYou can now run the Django server and test the LMS!")
    print("python manage.py runserver")

if __name__ == '__main__':
    create_sample_data()

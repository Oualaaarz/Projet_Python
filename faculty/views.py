from django.shortcuts import render, redirect 
from student.models import Student, Parent
from teacher.models import Teacher
from department.models import Department
from subject.models import Subject
from holidays.models import Holiday
from exams.models import Exam
from timetable.models import Timetable
from school.decorators import any_authenticated_required

def index(request): 
    return render(request, 'authentication/login.html')

@any_authenticated_required
def dashboard(request):
    # Count all entities
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    total_subjects = Subject.objects.count()
    total_holidays = Holiday.objects.count()
    total_exams = Exam.objects.count()
    total_timetable = Timetable.objects.count()
    
    # Get recent students
    recent_students = Student.objects.all().order_by('-id')[:5]
    
    # Get upcoming exams (sorted by date if available)
    upcoming_exams = Exam.objects.all().order_by('date')[:3]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'total_subjects': total_subjects,
        'total_holidays': total_holidays,
        'total_exams': total_exams,
        'total_timetable': total_timetable,
        'recent_students': recent_students,
        'upcoming_exams': upcoming_exams,
    }
    
    return render(request, 'Home/index.html', context) 
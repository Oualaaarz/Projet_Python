from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse 
from django.contrib import messages
from school.decorators import role_required, any_authenticated_required
from .models import Student, Parent 
from teacher.models import Teacher
from department.models import Department
from subject.models import Subject
from holidays.models import Holiday
from exams.models import Exam
from timetable.models import Timetable

@any_authenticated_required
def teacher_dashboard(request):
    if not (request.user.is_teacher or request.user.is_admin):
        messages.error(request, "Accès réservé aux enseignants et administrateurs.")
        return redirect('student_dashboard')
    # Gather statistics
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    total_subjects = Subject.objects.count()
    total_holidays = Holiday.objects.count()
    total_exams = Exam.objects.count()
    total_timetable = Timetable.objects.count()
    
    # Get recent students
    recent_students = Student.objects.all().order_by('-id')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'total_subjects': total_subjects,
        'total_holidays': total_holidays,
        'total_exams': total_exams,
        'total_timetable': total_timetable,
        'recent_students': recent_students,
    }
    return render(request, 'teacher/teacher-dashboard.html', context)

@any_authenticated_required
def student_dashboard(request):
    # Gather statistics
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    total_subjects = Subject.objects.count()
    total_holidays = Holiday.objects.count()
    total_exams = Exam.objects.count()
    total_timetable = Timetable.objects.count()
    
    # Get recent students
    recent_students = Student.objects.all().order_by('-id')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'total_subjects': total_subjects,
        'total_holidays': total_holidays,
        'total_exams': total_exams,
        'total_timetable': total_timetable,
        'recent_students': recent_students,
    }
    return render(request, 'students/student-dashboard.html', context)

@role_required('teacher', 'admin')
def student_list(request): 
    students = Student.objects.all()
    return render(request, 'students/students.html', {'student_list': students})

@role_required('admin')
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # Check permissions: admin can edit all, student can edit own
    if not (request.user.is_admin or (request.user.is_student and student.student_id == request.user.username)):
        messages.error(request, "Vous ne pouvez modifier que votre propre profil.")
        return redirect('student_list')

    parent = student.parent  # <-- AJOUTÉ pour le template

    if request.method == 'POST':
        # Mêmes champs qu'avant
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        student.religion = request.POST.get('religion')

        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        # Parent update
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')

        student.save()
        parent.save()

        messages.success(request, 'Student updated successfully')
        return redirect('student_list')

    return render(request, 'students/edit-student.html', {'student': student, 'parent': parent})

@any_authenticated_required
def view_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # Check permissions: admin can view all, teacher can view all, student can view only their own
    if request.user.is_student and student.student_id != request.user.username:
        messages.error(request, "Vous ne pouvez voir que votre propre profil.")
        return redirect('student_dashboard')

    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_subjects = Subject.objects.count()

    return render(request, 'students/student-details.html', {
        'student': student,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
    })
@role_required('admin')
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(request, 'students/delete-student.html', {'student': student})

@role_required('admin')
def add_student(request): 
    if request.method == 'POST': 
        # Récupérer les données de l'étudiant 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        student_id = request.POST.get('student_id') 
        gender = request.POST.get('gender') 
        date_of_birth = request.POST.get('date_of_birth') 
        student_class = request.POST.get('student_class') 
        joining_date = request.POST.get('joining_date') 
        mobile_number = request.POST.get('mobile_number') 
        admission_number = request.POST.get('admission_number') 
        section = request.POST.get('section') 
        student_image = request.FILES.get('student_image') 
 
        # Récupérer les données du parent 
        father_name = request.POST.get('father_name') 
        father_occupation = request.POST.get('father_occupation') 
        father_mobile = request.POST.get('father_mobile') 
        father_email = request.POST.get('father_email') 
        mother_name = request.POST.get('mother_name') 
        mother_occupation = request.POST.get('mother_occupation') 
        mother_mobile = request.POST.get('mother_mobile') 
        mother_email = request.POST.get('mother_email') 
        present_address = request.POST.get('present_address') 
        permanent_address = request.POST.get('permanent_address') 
        parent = Parent.objects.create( 
             father_name=father_name, 
            father_occupation=father_occupation, 
            father_mobile=father_mobile, 
            father_email=father_email, 
            mother_name=mother_name, 
            mother_occupation=mother_occupation, 
            mother_mobile=mother_mobile, 
            mother_email=mother_email, 
            present_address=present_address, 
            permanent_address=permanent_address 
        ) 
        student = Student.objects.create( 
            first_name=first_name, 
            last_name=last_name, 
            student_id=student_id, 
            gender=gender, 
            date_of_birth=date_of_birth, 
            student_class=student_class, 
            joining_date=joining_date, 
            mobile_number=mobile_number, 
            admission_number=admission_number, 
            section=section, 
            student_image=student_image, 
            parent=parent 
        )

        messages.success(request, 'Student added Successfully') 
        return redirect('student_list') 
    else: 
        return render(request, 'students/add-student.html')


 


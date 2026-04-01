from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject
from department.models import Department
from django.contrib import messages
from school.decorators import role_required, any_authenticated_required

# 🔴 LIST
@any_authenticated_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject/subject_list.html', {'subjects': subjects})


# 🔴 ADD
@role_required('teacher', 'admin')
def add_subject(request):
    departments = Department.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        department_id = request.POST.get('department')

        department = Department.objects.get(id=department_id)

        Subject.objects.create(
            name=name,
            department=department
        )

        messages.success(request, "Subject added successfully!")
        return redirect('subject_list')

    return render(request, 'subject/add_subject.html', {
        'departments': departments
    })


# 🔴 EDIT
@role_required('teacher', 'admin')
def edit_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    departments = Department.objects.all()

    if request.method == "POST":
        subject.name = request.POST.get('name')
        department_id = request.POST.get('department')

        subject.department = Department.objects.get(id=department_id)
        subject.save()

        messages.success(request, "Subject updated successfully!")
        return redirect('subject_list')

    return render(request, 'subject/edit_subject.html', {
        'subject': subject,
        'departments': departments
    })


# 🔴 DELETE
@role_required('teacher', 'admin')
def delete_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()

    messages.success(request, "Subject deleted successfully!")
    return redirect('subject_list')
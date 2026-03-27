from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from department.models import Department
from django.contrib import messages

# 🔴 LIST
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teacher_list.html', {'teachers': teachers})


# 🔴 ADD
def add_teacher(request):
    departments = Department.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        department_id = request.POST.get('department')

        department = Department.objects.get(id=department_id)

        Teacher.objects.create(
            name=name,
            email=email,
            department=department
        )

        messages.success(request, "Teacher added successfully!")
        return redirect('teacher_list')

    return render(request, 'teacher/add_teacher.html', {
        'departments': departments
    })


# 🔴 EDIT
def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    departments = Department.objects.all()

    if request.method == "POST":
        teacher.name = request.POST.get('name')
        teacher.email = request.POST.get('email')
        department_id = request.POST.get('department')

        teacher.department = Department.objects.get(id=department_id)
        teacher.save()

        messages.success(request, "Teacher updated successfully!")
        return redirect('teacher_list')

    return render(request, 'teacher/edit_teacher.html', {
        'teacher': teacher,
        'departments': departments
    })


# 🔴 DELETE
def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.delete()

    messages.success(request, "Teacher deleted successfully!")
    return redirect('teacher_list')
def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'teacher/teacher_detail.html', {'teacher': teacher})
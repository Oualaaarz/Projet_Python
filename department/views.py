from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from school.decorators import admin_required, any_authenticated_required
from .models import Department

@any_authenticated_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department/department_list.html', {'departments': departments})

@admin_required
def add_department(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Department.objects.create(name=name)
        messages.success(request, "Department added successfully!")
        return redirect('department_list')

    return render(request, 'department/add_department.html')

@admin_required
def edit_department(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == "POST":
        department.name = request.POST.get('name')
        department.save()
        messages.success(request, "Department updated successfully!")
        return redirect('department_list')

    return render(request, 'department/edit_department.html', {'department': department})

@admin_required
def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == "POST":
        department.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('department_list')

    return render(request, 'department/delete_department.html', {'department': department})
from django.shortcuts import render, redirect
from .models import Department

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department/department_list.html', {'departments': departments})

def add_department(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Department.objects.create(name=name)
        return redirect('department_list')

    return render(request, 'department/add_department.html')
from django.shortcuts import render, redirect, get_object_or_404
from .models import Timetable
from django.contrib import messages
from school.decorators import role_required, any_authenticated_required

@any_authenticated_required
def timetable_list(request):
    data = Timetable.objects.all()
    return render(request, 'timetable/time-table.html', {'data': data})

@role_required('teacher', 'admin')
def add_timetable(request):
    if request.method == 'POST':
        Timetable.objects.create(
            day=request.POST['day'],
            subject=request.POST['subject'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time']
        )
        messages.success(request, "Timetable added!")
        return redirect('timetable_home')  # <-- corrigé ici
    return render(request, 'timetable/add-time-table.html')

@role_required('teacher', 'admin')
def edit_timetable(request, id):
    t = get_object_or_404(Timetable, id=id)
    if request.method == 'POST':
        t.day = request.POST['day']
        t.subject = request.POST['subject']
        t.start_time = request.POST['start_time']
        t.end_time = request.POST['end_time']
        t.save()
        messages.success(request, "Timetable updated!")
        return redirect('timetable_home')  # <-- corrigé ici
    return render(request, 'timetable/edit-time-table.html', {'t': t})

@role_required('teacher', 'admin')
def delete_timetable(request, id):
    t = get_object_or_404(Timetable, id=id)
    t.delete()
    messages.success(request, "Timetable deleted!")
    return redirect('timetable_home')
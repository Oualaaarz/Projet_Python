from django.shortcuts import render, redirect, get_object_or_404
from .models import Holiday
from django.contrib import messages
from school.decorators import admin_required

@admin_required
def holidays_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holidays.html', {'holidays': holidays})

@admin_required
def add_holiday(request):
    if request.method == 'POST':
        Holiday.objects.create(
            title=request.POST['title'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            description=request.POST['description']
        )
        messages.success(request, "Holiday added!")
        return redirect('holidays_home')  # <-- corrigé
    return render(request, 'holidays/add-holiday.html')

@admin_required
def edit_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    if request.method == 'POST':
        holiday.title = request.POST['title']
        holiday.start_date = request.POST['start_date']
        holiday.end_date = request.POST['end_date']
        holiday.description = request.POST['description']
        holiday.save()
        messages.success(request, "Holiday updated!")
        return redirect('holidays_home')  # <-- corrigé
    return render(request, 'holidays/edit-holiday.html', {'holiday': holiday})

@admin_required
def delete_holiday(request, id):
    holiday = get_object_or_404(Holiday, id=id)
    holiday.delete()
    messages.success(request, "Holiday deleted!")
    return redirect('holidays_home')  # <-- corrigé
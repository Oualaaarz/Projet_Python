from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Décorateur pour restreindre l'accès aux administrateurs"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def teacher_required(view_func):
    """Décorateur pour restreindre l'accès aux enseignants et administrateurs"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_teacher or request.user.is_admin):
            messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def student_or_admin_required(view_func):
    """Décorateur pour restreindre l'accès aux étudiants et administrateurs"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_student or request.user.is_admin):
            messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def any_authenticated_required(view_func):
     
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

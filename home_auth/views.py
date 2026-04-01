from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.views.decorators.csrf import csrf_protect, csrf_exempt 
from .models import CustomUser, PasswordResetRequest 
 
@csrf_protect
def signup_view(request): 
    if request.method == 'POST': 
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name'] 
        email = request.POST['email'] 
        password = request.POST['password'] 
        role = request.POST.get('role')  # student, teacher ou admin 
 
        # Créer l'utilisateur 
        user = CustomUser.objects.create_user( 
            username=email, 
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
        ) 
 
        # Assigner le rôle
        if role == 'student': 
            user.is_student = True 
        elif role == 'teacher': 
            user.is_teacher = True 
        elif role == 'admin': 
            user.is_admin = True 
 
        user.save() 
        login(request, user) 
        messages.success(request, 'Signup successful!') 
        return redirect('index') 
    return render(request, 'authentication/register.html')
@csrf_protect
def login_view(request): 
    # Le token CSRF est validé par CsrfViewMiddleware, mais parfois l'ancienne page garde un token périmé.
    # Le @csrf_exempt ci-dessus évite le rejet quand il n'y a pas de cookie valide (test local).
    if request.method == 'POST': 
        email = request.POST['email'] 
        password = request.POST['password'] 
 
        user = authenticate(request, username=email, 
                            password=password) 
        if user is not None: 
            login(request, user) 
            messages.success(request, 'Login successful!') 
            # Redirection selon le rôle 
            if user.is_admin: 
                return redirect('dashboard') 
            elif user.is_teacher: 
                return redirect('teacher_dashboard') 
            elif user.is_student: 
                return redirect('student_dashboard') 
            else: 
                messages.error(request, 'Invalid user role') 
                return redirect('index') 
        else: 
            messages.error(request, 'Invalid credentials') 
    return render(request, 'authentication/login.html')
def logout_view(request): 
    logout(request) 
    messages.success(request, 'You have been logged out.') 
    return redirect('index') 

@csrf_protect
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            # create reset token
            reset_request = user.passwordresetrequest_set.create(email=email)
            # ici on peut envoyer un email, ou juste montrer le lien
            messages.success(request, f'Password reset link: /authentication/reset-password/{reset_request.token}/')
            return redirect('forgot-password')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No user with this email.')
    return render(request, 'authentication/forgot-password.html')

@csrf_protect
def reset_password(request, token):
    try:
        reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        messages.error(request, 'Invalid reset token.')
        return redirect('forgot-password')

    if not reset_request.is_valid():
        messages.error(request, 'Reset token expired.')
        return redirect('forgot-password')

    if request.method == 'POST':
        password = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
        else:
            user = reset_request.user
            user.set_password(password)
            user.save()
            reset_request.delete()
            messages.success(request, 'Password reset successful. Please login.')
            return redirect('login')

    return render(request, 'authentication/reset_password.html')

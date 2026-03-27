from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('add/', views.add_teacher, name='teacher_add'),  # compatibility alias
    path('edit/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('edit/<int:id>/', views.edit_teacher, name='teacher_edit'),  # compatibility alias
    path('delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('teacher/<int:id>/', views.teacher_detail, name='teacher_detail'),
]
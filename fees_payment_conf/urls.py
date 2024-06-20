"""fees_payment_conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from fees_payment_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('login/', views.custom_login, name='login'),
    
    # Student URLs
    path('student/dasboard', views.student_dashboard, name='student_dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/new/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/new/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Semester URLs
    path('semesters/', views.semester_list, name='semester_list'),
    path('semesters/<int:pk>/', views.semester_detail, name='semester_detail'),
    path('semesters/new/', views.semester_create, name='semester_create'),
    path('semesters/<int:pk>/edit/', views.semester_update, name='semester_update'),
    path('semesters/<int:pk>/delete/', views.semester_delete, name='semester_delete'),

    # Fee URLs
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/<int:pk>/', views.fee_detail, name='fee_detail'),
    path('fees/new/', views.fee_create, name='fee_create'),
    path('fees/<int:pk>/edit/', views.fee_update, name='fee_update'),
    path('fees/<int:pk>/delete/', views.fee_delete, name='fee_delete'),

    # Payment URLs
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
    path('payments/new/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/edit/', views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),

    # Receipt URLs
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('receipts/<int:pk>/', views.receipt_detail, name='receipt_detail'),
    path('receipts/new/', views.receipt_create, name='receipt_create'),
    path('receipts/<int:pk>/edit/', views.receipt_update, name='receipt_update'),
    path('receipts/<int:pk>/delete/', views.receipt_delete, name='receipt_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



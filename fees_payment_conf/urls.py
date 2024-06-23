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
    path('dashboard', views.student_dashboard, name='student_dashboard'),
    path('students/new/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    path('tuition', views.student_tuition, name='student_tuition'),
    path('payment_receipt', views.payment_receipt, name='payment_receipt'),
    path('pay-fees/', views.pay_fees, name='pay_fees'),
    path('student-info', views.student_info, name='student_info'),

    # Fee URLs
    path('fees/new/', views.fee_create, name='fee_create'),
    path('fees/<int:pk>/edit/', views.fee_update, name='fee_update'),
    path('fees/<int:pk>/delete/', views.fee_delete, name='fee_delete'),

    # Payment URLs
    path('<str:ref>/', views.verify_payment, name='verify_payment'),  
    path('make_payment', views.make_payment, name='make_payment'),  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



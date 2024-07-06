from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Academic_Year)
admin.site.register(Facaulty)
admin.site.register(StudentCategory)
admin.site.register(Student)
admin.site.register(Fee)
admin.site.register(Payment)
admin.site.register(Receipt)

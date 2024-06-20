from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Course, Semester, Fee, Payment, Receipt

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Fee)
admin.site.register(Payment)
admin.site.register(Receipt)

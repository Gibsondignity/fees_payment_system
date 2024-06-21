import secrets
from django.db import models
from .paystack import PayStack
# Create your models here.
from django.db import models
from django.contrib.auth.models import User



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    enrollment_date = models.DateField()
    
    def __str__(self):
        return f"{self.full_name} ({self.student_id})"




class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    
    def __str__(self):
        return self.course_name




class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
    ]
    
    name = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name




class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True,null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.course.course_name} - {self.semester.name}: {self.amount}"





class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True,null=True)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50, unique=True)
    payment_method = models.CharField(max_length=50, blank=True,null=True)  # e.g., 'Credit Card', 'Mobile Money', etc.
    ref = models.CharField(max_length=50, blank=True,null=True)
    verify = models.BooleanField(default=False)
    status = models.CharField(max_length=20, null=True, blank=True, default='pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"Payment by {self.student.full_name} on {self.payment_date}"
    
    def verify_payment(self):
        payment = PayStack()
        status, result = payment.verify_payment(self.ref)
        if status:
            self.status = status
            if result['amount'] == 100*self.amount_paid:
                self.verify = True
            self.save()

        if self.verify:
            return True
        return False
    
    
    def save(self, *args, **kwargs):
        if not self.ref:
            while not self.ref:
                ref = secrets.token_urlsafe(20)
                object_with_similar_ref = Payment.objects.filter(ref=ref)
                if not object_with_similar_ref:
                    self.ref = ref


        super().save(*args, **kwargs)





class Receipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.payment.student.full_name}"






    
        
    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets


from fees_payment_app.paystack import PayStack

import datetime

class Academic_Year(models.Model):
    YEARS = [(r, r) for r in range(datetime.datetime.now().year, 2020, -1)]
    year = models.CharField(max_length=20)
    date_created = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.get_year_display()
    

class Facaulty(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name



class StudentCategory(models.Model):
    category_name = models.CharField(max_length=50)  # e.g., Freshmen, Top-up, Continuing
    description = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.category_name



class Student(models.Model):
    level_choices = (
        ('Level 100', 'Level 100'), 
        ('Level 200', 'Level 200'), 
        ('Level 300', 'Level 300'), 
        ('Level 400', 'Level 400')
    )
    nationality_choices = (
        ('Ghanaian', 'Ghanaian'), 
        ('International Student', 'International Student')
    )
    category_choices = (
        ('Freshmen', 'Freshmen'), 
        ('Top-up', 'Top-up'), 
        ('Continuing', 'Continuing')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    enrollment_date = models.DateField(null=True)
    completion_date = models.DateField(null=True)
    facaulty = models.ForeignKey(Facaulty, on_delete=models.CASCADE, null=True, blank=True)
    entry_level = models.CharField(max_length=255, choices=level_choices, null=True)
    current_level = models.CharField(max_length=255, choices=level_choices, null=True)
    nationality = models.CharField(max_length=255, choices=nationality_choices, null=True)
    student_category = models.CharField(max_length=255, choices=category_choices, null=True)
    date_created = models.DateField(auto_now=True, null=True)
    date_updated = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


    
    
class Fee(models.Model):
    
    nationality_choices = (
        ('Ghanaian', 'Ghanaian'), 
        ('International Student', 'International Student')
    )
    
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    tuition_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nationality = models.CharField(max_length=255, choices=nationality_choices, null=True)
    date_created = models.DateField(auto_now=True, null=True)
    date_updated = models.DateField(auto_now_add=True, null=True)
    
    def add_total_fees(self):
        self.total_fees = self.tuition_amount + self.other_charges
        
    def save(self, *args, **kwargs):
        self.add_total_fees()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.facaulty.name} | {self.academic_year} Acd. Year | Fee: {self.total_fees}"



class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True,null=True)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_date = models.DateTimeField(auto_now_add=True, null=True)
    transaction_id = models.CharField(max_length=50, unique=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True,null=True)  
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
    receipt_number = models.CharField(max_length=50, unique=True, null=True)
    issue_date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.payment.student.full_name}"






    
        
    
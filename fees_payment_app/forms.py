from django import forms
from .models import Student, Fee, Payment, Receipt

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'

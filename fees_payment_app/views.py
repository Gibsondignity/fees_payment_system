# Create your views here.
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Student, Fee, Payment, Receipt
from .forms import StudentForm, FeeForm, PaymentForm, ReceiptForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum


def index(request):
    
    return render(request, 'index.html')


def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # if user.is_superuser:
            #     return redirect('/')
            # else:
            #     return redirect('/')
            return redirect(reverse('student_dashboard'))
        else:
            messages.error(request, "Invalid username or password.")
    if request.user.is_authenticated:
        return redirect(reverse('student_dashboard'))
    return render(request, 'login.html')




# Student Views
def student_dashboard(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    fees = Fee.objects.filter(facaulty=student.facaulty, level=student.current_level, student_category=student.student_category)
    payments = Payment.objects.filter(student=student)

    total_fees = fees.aggregate(Sum('tuition_amount'))['tuition_amount__sum'] or 0
    total_payments = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    arrears = total_fees - total_payments

    context = {
        'student': student,
        'fees': fees,
        'payments': payments,
        'total_fees': total_fees,
        'total_payments': total_payments,
        'arrears': arrears
    }
    return render(request, 'student/dashboard.html')



def student_tuition(request):
    
    
    return render(request, "student/student_tuition.html")


def pay_fees(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    fees = Fee.objects.filter(facaulty=student.facaulty, level=student.current_level, student_category=student.student_category)

    context = {'student':student, 'fees':fees}
        
    return render(request, "student/initiate_payment.html", context)



def student_fee_history(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    fees = Fee.objects.filter(facaulty=student.facaulty, level=student.current_level, student_category=student.student_category)
    payments = Payment.objects.filter(student=student)

    total_fees = fees.aggregate(Sum('tuition_amount'))['tuition_amount__sum'] or 0
    total_payments = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    arrears = total_fees - total_payments

    context = {
        'student': student,
        'fees': fees,
        'payments': payments,
        'total_fees': total_fees,
        'total_payments': total_payments,
        'arrears': arrears
    }

    return render(request, 'student_fee_history.html', context)



def make_payment(request):
    amount = request.POST['amount']
    fee = request.POST['fees']
    
    fees = Fee.objects.filter(id=fee).first()
    
    print(fees.tuition_amount, fees.other_charges)
    payment = Payment()
    
    # context = {'ref': payment.ref,
    #             'amount': payment.amount),
    #                 'email': student,
    #                 'payment_date': payment.payment_date,
    #                 'key': settings.PAYSTACK_PUBLIC_KEY,
    #                 'id': id,
    #             }
    
    context = {'fees': fees}
    return render(request, "student/pay_fees.html", context)






def student_info(request):
    
    
    return render(request, "student/student-info.html")



def verify_payment(request, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)

    verified = payment.verify_payment()

    if verified:
        return HttpResponse('Payment was successful.')
    else:
        return HttpResponse('Payment was not successful.')
    
    
   
   
def payment_receipt(request):
    
    return render(request, 'student/payment_receipt.html')   
   
   
 

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})



def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})




def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})



def fee_create(request):
    if request.method == "POST":
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save()
            return redirect('fee_detail', pk=fee.pk)
    else:
        form = FeeForm()
    return render(request, 'fee_form.html', {'form': form})




def fee_update(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == "POST":
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            fee = form.save()
            return redirect('fee_detail', pk=fee.pk)
    else:
        form = FeeForm(instance=fee)
    return render(request, 'fee_form.html', {'form': form})



def fee_delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == "POST":
        fee.delete()
        return redirect('fee_list')
    return render(request, 'fee_confirm_delete.html', {'fee': fee})



def calculate_arrears(student):
    # Get all fees for the student
    fees = Fee.objects.filter(course__enrollment__student=student)
    total_fees = fees.aggregate(Sum('amount'))['amount__sum'] or 0

    # Get all payments made by the student
    payments = Payment.objects.filter(student=student)
    total_payments = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    # Calculate arrears
    arrears = total_fees - total_payments
    return arrears





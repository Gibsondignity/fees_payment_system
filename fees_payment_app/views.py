# Create your views here.
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Student, Fee, Payment, Receipt
from .forms import StudentForm, FeeForm, PaymentForm, ReceiptForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

            return redirect(reverse('student_dashboard'))
        else:
            messages.error(request, "Invalid ID or password.")
    if request.user.is_authenticated:
        return redirect(reverse('student_dashboard'))
    return render(request, 'login.html')

@login_required
def logout_user(request):
    """
    Log out the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the login page.
    """
    logout(request)
    return redirect('login')
@login_required
def reset_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        print(current_password, new_password1, new_password2)
        user = authenticate(request, username=current_password, password=current_password)
        if user is not None:
            if new_password1 == new_password2:
                request.user.set_password(new_password1)
                request.user.save()
                return redirect(reverse('login'))
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Invalid current password.")

    return redirect(reverse('student_info'))



# Student Views
@login_required
def student_dashboard(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    fees = Fee.objects.filter(facaulty=student.facaulty, level=student.current_level, nationality=student.nationality)
    payments = Payment.objects.filter(student=student, status=True)
    payment_count = Payment.objects.filter(student=student, status=True).count()

    total_fees = fees.aggregate(Sum('total_fees'))['total_fees__sum'] or 0
    total_payments = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    arrears = 0
    for fee in fees:
        payment = payments.filter(fee=fee).first()
        if payment:
            arrears += fee.total_fees - payment.amount_paid
        else:
            arrears += fee.total_fees

    context = {
        'fees': fees,
        'payments': payments,
        'total_fees': total_fees,
        'total_payments': total_payments,
        'arrears': arrears,
        'payment_count': payment_count
    }
    return render(request, 'student/dashboard.html', context)




@login_required
def student_tuition(request):
    
    user = request.user
    student = get_object_or_404(Student, user=user)
    fees = Fee.objects.filter(facaulty=student.facaulty, level=student.current_level, student_category=student.student_category)
    
    payments = Payment.objects.filter(student=student, status=True)
    total_fees = fees.aggregate(Sum('total_fees'))['total_fees__sum'] or 0
    total_payments = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    arrears = Decimal(0)
    
    context = {'student':student, 'fees':fees, 'arrears':arrears}
    
    return render(request, "student/student_tuition.html", context)




@login_required
def pay_fees(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    fees = Fee.objects.filter(facaulty=student.facaulty, level=student.current_level, student_category=student.student_category)

    context = {'student':student, 'fees':fees}
        
    return render(request, "student/initiate_payment.html", context)


@login_required
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


@login_required
def student_info(request):
    
    student = Student.objects.filter(user=request.user).first()
    
    return render(request, "student/student-info.html", {'student': student})


# Payment Views
@login_required
def make_payment(request):
    if request.method == "POST":
        percentage = request.POST.get('percentage')
        fees = request.POST.get('fees')
        student = request.user.student
        fee_instance = Fee.objects.filter(pk=fees).first()
        amount = fee_instance.total_fees * Decimal(percentage) / 100
        
        payment = Payment()
        payment.amount_paid = amount
        payment.student = student
        payment.fee = fee_instance
        payment.save()
        
        payment.save()

        context = {     
                   'ref': payment.ref,
                    'amount': payment.amount_paid,
                    'email': request.user.student.email,
                    'fee': payment.fee,
                    'payment_date': payment.payment_date,
                    'key': settings.PAYSTACK_PUBLIC_KEY,
                    'id': id,
                    'amount': amount, 
                    'fee_instance': fee_instance
            }
        
    else:
        messages.error(request, "Method not allowed!")
        return redirect(reverse('pay_fees'))
    print(context)
    return render(request, "student/pay_fees.html", context)


@login_required
def verify_payment(request, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)

    verified = payment.verify_payment()

    if verified:
        messages.success(request, 'Payment was successful.')
        return redirect('student_dashboard')
    else:
        messages.error(request, 'Payment was not successful.')
        return redirect('student_dashboard')
    
    
   
@login_required   
def payment_receipt(request):
    
    return render(request, 'student/payment_receipt.html')   
   
   
 
 
 
 
 
 
 
 
 
# Superuser views


def superuser_login(request):
    if request.method == 'GET':
        return render(request, 'dashboard/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back {username}!')
                return redirect('superuser_dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
                return render(request, 'dashboard/login.html')
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'dashboard/login.html')


def superuser_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('superuser_login')



@login_required(login_url='superuser_login')
def superuser_dashboard(request):
    fees = Fee.objects.aggregate(total_fees=Sum('total_fees'))['total_fees'] or 0
    payments = Payment.objects.filter(status=True).aggregate(total_payments=Sum('amount_paid'))['total_payments'] or 0
    payment_count = Payment.objects.filter(status=True).count()

    context = {'fees': fees, 'payments': payments, 'payment_count': payment_count}
    return render(request, 'dashboard/dashboard.html',)




# Admin Student View
def admit_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'dashboard/admit_student.html', {'form': form})



def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})




def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})



def add_fees(request):
    if request.method == "POST":
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save()
            return redirect('fee_detail', pk=fee.pk)
    else:
        form = FeeForm()
    return render(request, 'dashboard/add_fees.html', {'form': form})




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






# Facauty Views

def facauty(request):
    
    return render(request, 'dashboard/facauty.html')



# Academic Year Views

def academic_year(request):
    
    return render(request, 'dashboard/academic_year.html')




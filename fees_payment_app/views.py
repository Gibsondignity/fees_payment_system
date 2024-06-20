# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Student, Course, Semester, Fee, Payment, Receipt
from .forms import StudentForm, CourseForm, SemesterForm, FeeForm, PaymentForm, ReceiptForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages





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
    
    return render(request, 'student/dashboard.html')



def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})




def fees_collection(request):
    
    
    return render(request, "student/fees-collection.html")


def pay_fees(request):
    
    
    return render(request, "student/pay_fees.html")




def fees_receipt(request):
    
    
    return render(request, "student/fees-receipt.html")




def profile(request):
    
    
    return render(request, "student/profile.html")





def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': student})



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










# Course Views
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course_detail.html', {'course': course})

def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect('course_list')
    return render(request, 'course_confirm_delete.html', {'course': course})


# Semester Views
def semester_list(request):
    semesters = Semester.objects.all()
    return render(request, 'semester_list.html', {'semesters': semesters})

def semester_detail(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    return render(request, 'semester_detail.html', {'semester': semester})

def semester_create(request):
    if request.method == "POST":
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save()
            return redirect('semester_detail', pk=semester.pk)
    else:
        form = SemesterForm()
    return render(request, 'semester_form.html', {'form': form})

def semester_update(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == "POST":
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            semester = form.save()
            return redirect('semester_detail', pk=semester.pk)
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'semester_form.html', {'form': form})

def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == "POST":
        semester.delete()
        return redirect('semester_list')
    return render(request, 'semester_confirm_delete.html', {'semester': semester})


# Fee Views
def fee_list(request):
    fees = Fee.objects.all()
    return render(request, 'fee_list.html', {'fees': fees})

def fee_detail(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    return render(request, 'fee_detail.html', {'fee': fee})

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


# Payment Views
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})

def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'payment_detail.html', {'payment': payment})

def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return redirect('payment_detail', pk=payment.pk)
    else:
        form = PaymentForm()
    return render(request, 'payment_form.html', {'form': form})

def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            return redirect('payment_detail', pk=payment.pk)
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payment_form.html', {'form': form})

def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        payment.delete()
        return redirect('payment_list')
    return render(request, 'payment_confirm_delete.html', {'payment': payment})


# Receipt Views
def receipt_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})

def receipt_detail(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    return render(request, 'receipt_detail.html', {'receipt': receipt})

def receipt_create(request):
    if request.method == "POST":
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()
            return redirect('receipt_detail', pk=receipt.pk)
    else:
        form = ReceiptForm()
    return render(request, 'receipt_form.html', {'form': form})

def receipt_update(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    if request.method == "POST":
        form = ReceiptForm(request.POST, instance=receipt)
        if form.is_valid():
            receipt = form.save()
            return redirect('receipt_detail', pk=receipt.pk)
    else:
        form = ReceiptForm(instance=receipt)
    return render(request, 'receipt_form.html', {'form': form})

def receipt_delete(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    if request.method == "POST":
        receipt.delete()
        return redirect('receipt_list')
    return render(request, 'receipt_confirm_delete.html', {'receipt': receipt})

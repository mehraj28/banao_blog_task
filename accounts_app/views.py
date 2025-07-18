from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import PatientSignUpForm, DoctorSignUpForm, BlogPostForm, AppointmentForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Appointment, BlogPost
from .google_calendar import create_calendar_event
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from .utils import send_calendar_instructions


def home(request):
    return render(request, 'home.html')


def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Patient'})


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            doctor_email = user.email
            doctor_name = user.get_full_name()
            send_calendar_instructions(doctor_email, doctor_name)
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSignUpForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Doctor'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')
            elif user.is_doctor:
                return redirect('doctor_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


User = get_user_model()


@login_required
def patient_dashboard(request):
    doctors = User.objects.filter(is_doctor=True)
    appointments = Appointment.objects.filter(patient=request.user)
    posts = BlogPost.objects.filter(draft=False)
    for post in posts:
        post.summary = ' '.join(post.summary.split()[:15]) + '...'
    return render(request, 'patient_dashboard.html', {
        'user': request.user,
        'doctors': doctors,
        'appointments': appointments,
        'posts': posts,
    })


@login_required
def doctor_dashboard(request):
    doctor = request.user
    appointments = Appointment.objects.filter(doctor=doctor)
    posts = BlogPost.objects.filter(author=doctor)
    context = {
        'user': doctor,
        'appointments': appointments,
        'posts': posts,
    }
    return render(request, 'doctor_dashboard.html', context)


# blog
@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('doctor_dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'create_blog_post.html', {'form': form})


# edit blog
@login_required
def edit_blog_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'edit_blog_post.html', {'form': form, 'blog_post': blog_post})


# Appointment
User = get_user_model()


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id, is_doctor=True)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.date = form.cleaned_data['date']
            appointment.start_time = form.cleaned_data['start_time']

            # Combine date and time to form datetime objects
            start_datetime = timezone.make_aware(datetime.combine(appointment.date, appointment.start_time))
            appointment.start_time = start_datetime

            # Calculate end time (45 minutes later)
            appointment.end_time = start_datetime + timedelta(minutes=45)

            appointment.save()
            create_calendar_event(appointment, doctor.email)
            return redirect('appointment_details', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})


@login_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_details.html', {'appointment': appointment})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Patient, Doctor
from django.contrib.auth.decorators import login_required


def patient_sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        profile_picture = request.FILES.get('profile_picture')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('patient_sign_up')

        # Create user
        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        # Create patient profile
        patient = Patient.objects.create(user=user, first_name=first_name, last_name=last_name,
                                         profile_picture=profile_picture, address_line1=address_line1, city=city, state=state, pincode=pincode)
        patient.save()

        messages.success(request, "Signup successful!")
        return redirect('home')
    return render(request, 'sign_up.html')


def doctor_sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        profile_picture = request.FILES.get('profile_picture')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('doctor_sign_up')

        # Create user
        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        # Create doctor profile
        doctor = Doctor.objects.create(user=user, first_name=first_name, last_name=last_name,
                                       profile_picture=profile_picture, address_line1=address_line1, city=city, state=state, pincode=pincode)
        doctor.save()

        messages.success(request, "Signup successful!")
        return redirect('home')
    return render(request, 'sign_up.html')


def home(request):
    if request.user.is_authenticated:
        u = User.objects.filter(username=request.user)
        u = u[0]
        return render(request, 'index.html', {'users': u})
    return redirect('sign_in')


def logout(request):
    auth.logout(request)
    return redirect('sign_in')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is linked to a Patient instance
            if Patient.objects.filter(user=user).exists():
                return redirect('home')
            # Check if the user is linked to a Doctor instance
            elif Doctor.objects.filter(user=user).exists():
                return redirect('home')
            # If user is not linked to either Patient or Doctor instance, handle accordingly
            else:
                messages.error(
                    request, "You are not authorized to access this dashboard.")
                return redirect('sign_in')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('sign_in')
    return render(request, 'sign_in.html')

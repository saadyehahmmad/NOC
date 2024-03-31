from django.shortcuts import render, redirect , get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import AppointmentRequest, Appointment
from .forms import AppointmentRequestForm
from users.models import Profile
from django.utils import timezone
from notification.models import Notification

@login_required
def appointment_requests_view(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
        return redirect('login')

    user_profile = request.user.profile

    if user_profile.user_type != 'nurse':
        return redirect('/home/')

    appointment_requests = AppointmentRequest.objects.filter(receiver=request.user, is_active=True)

    return render(request, 'appointment_requests.html', {'appointment_requests': appointment_requests})

@login_required
def send_appointment_request(request):
    if request.method == "POST":
        form = AppointmentRequestForm(request.POST, user=request.user)


        if form.is_valid():
            appointment_request = form.save(commit=False)
            appointment_request.sender = request.user
            appointment_request.save()

            if appointment_request:
                notify = Notification( int(appointment_request.id),text_preview=form, sender=request.user, user=appointment_request.receiver,  notification_type=8)
                notify.save()
            return JsonResponse({'response': "Appointment request sent."})
    else:
        form = AppointmentRequestForm(user=request.user)
        # Filter the queryset for receiver field to include only nurses
        

    return render(request, "send_appointment_request.html", {'form': form })



@login_required
def accept_appointment_request(request, appointment_request_id):
    try:
        appointment_request = AppointmentRequest.objects.get(pk=appointment_request_id)
        if appointment_request.receiver == request.user:
            appointment_request.accept()
            return JsonResponse({'response': "Appointment request accepted."})
        else:
            return JsonResponse({'response': "You are not authorized to accept this appointment request."})
    except AppointmentRequest.DoesNotExist:
        return JsonResponse({'response': "Appointment request does not exist."})

@login_required
def decline_appointment_request(request, appointment_request_id):
    try:
        appointment_request = AppointmentRequest.objects.get(pk=appointment_request_id)
        if appointment_request.receiver == request.user:
            appointment_request.decline()
            return JsonResponse({'response': "Appointment request declined."})
        else:
            return JsonResponse({'response': "You are not authorized to decline this appointment request."})
    except AppointmentRequest.DoesNotExist:
        return JsonResponse({'response': "Appointment request does not exist."})

@login_required
def upcoming_appointments(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.user_type != 'nurse':
        return redirect('/home/')

    upcoming_appointments = Appointment.objects.filter(nurse=request.user)

    return render(request, 'upcoming_appointments.html', {'upcoming_appointments': upcoming_appointments})

@login_required
def my_appointments(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.user_type != 'patient':
        return redirect('/home/')

    appointment_requests = AppointmentRequest.objects.filter(sender=request.user)

    return render(request, 'my_appointments.html', {'appointment_requests': appointment_requests})

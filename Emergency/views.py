from django.shortcuts import render, redirect , get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import EmergencyRequest, Emergency
from users.models import Profile
from django.utils import timezone
from notification.models import Notification
import math
import logging
from django.http import JsonResponse
import json
from django.db.models import Min

def Distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km


@login_required
def update_profile_status(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        data = json.loads(request.body)
        print("Received data:", data)  # Debugging statement
        status = data.get('status', False)
        print("New status:", status)  # Debugging statement
        location = data.get('location', None)
        print("location:", location)  # Debugging statement
        user_profile.is_available_for_emergencies = status
        user_profile.location = location
        user_profile.save()
        return JsonResponse({'message': 'Profile status updated successfully'}, status=200)
    else:
        print("Invalid request")  # Debugging statement
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
@login_required
def Emergency_requests_view(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
        return redirect('login')

    user_profile = request.user.profile

    if user_profile.user_type != 'nurse':
        return redirect('/home/')

    Emergency_requests = EmergencyRequest.objects.filter(receiver=request.user, is_active=True)
    return render(request, 'Emergency_requests.html', {'Emergency_requests': Emergency_requests})



logger = logging.getLogger(__name__)


@login_required
def send_Emergency_request(request):
    if request.method == "POST":
        sender = request.user
        location = request.POST.get('location', '')
        note = request.POST.get('note', '')
        date_time = timezone.now()  # Set date_time to current time in Amman

        # Retrieve all nurses who are available for emergencies
        available_nurses = Profile.objects.filter(is_available_for_emergencies=True).exclude(user=sender)

        if available_nurses.exists():
            min_distance = float('inf')  # Initialize with a large value
            nearest_nurse = None

            sender_lat, sender_lon = map(float, location.split(','))

            # Iterate through available nurses to find the nearest one
            for nurse_profile in available_nurses:
                receiver_lat, receiver_lon = map(float, nurse_profile.location.split(','))
                distance = Distance(sender_lat, sender_lon, receiver_lat, receiver_lon)

                # Update nearest nurse if a closer one is found
                if distance < min_distance:
                    min_distance = distance
                    nearest_nurse = nurse_profile.user

            if nearest_nurse:
                try:
                    # Create EmergencyRequest object and assign receiver
                    emergency_request = EmergencyRequest.objects.create(
                        sender=sender,
                        receiver=nearest_nurse,
                        location=location,
                        note=note,
                        date_time=date_time,
                        distance=min_distance  # Add the distance attribute
                    )

                    # Log success message
                    logger.info(f"Emergency request sent successfully: {emergency_request}")

                    # Notify the nurse or perform any additional actions here
                    notify = Notification(
                        int(emergency_request.id),
                        text_preview="emergency",
                        sender=request.user,
                        user=emergency_request.receiver,
                        notification_type=9
                    )
                    notify.save()

                    return JsonResponse({'response': "Emergency request sent.", 'emergency_request_id': emergency_request.id})
                except Exception as e:
                    # Log any exceptions that occur during object creation
                    logger.error(f"Error creating EmergencyRequest: {e}")
                    return JsonResponse({'error': "An error occurred while processing the emergency request."}, status=500)
            else:
                # Log error if no nearest nurse is available
                logger.error("No nearest nurse available.")
                return JsonResponse({'error': "No nearest nurse available."}, status=400)
        else:
            # Log error if no nurses are available for emergencies
            logger.error("No nurses available for emergencies.")
            return JsonResponse({'error': "No nurses available for emergencies."}, status=400)
    else:
        # Return error response if method is not POST
        return render(request, 'send_Emergency_request.html')


@login_required
def accept_Emergency_request(request, Emergency_request_id):
    try:
        Emergency_request = EmergencyRequest.objects.get(pk=Emergency_request_id)
        if Emergency_request.receiver == request.user:
            Emergency_request.accept()
            return JsonResponse({'response': "Emergency request accepted."})
        else:
            return JsonResponse({'response': "You are not authorized to accept this Emergency request."})
    except EmergencyRequest.DoesNotExist:
        return JsonResponse({'response': "Emergency request does not exist."})

@login_required
def decline_Emergency_request(request, Emergency_request_id):
    try:
        Emergency_request = EmergencyRequest.objects.get(pk=Emergency_request_id)
        if Emergency_request.receiver == request.user:
            Emergency_request.decline()
            return JsonResponse({'response': "Emergency request declined."})
        else:
            return JsonResponse({'response': "You are not authorized to decline this Emergency request."})
    except EmergencyRequest.DoesNotExist:
        return JsonResponse({'response': "Emergency request does not exist."})

@login_required
def upcoming_Emergency(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.user_type != 'nurse':
        return redirect('/home/')
    
    upcoming_Emergencys = Emergency.objects.filter(nurse=request.user)

    return render(request, 'upcoming_Emergency.html', {'upcoming_Emergencys': upcoming_Emergencys})

@login_required
def my_Emergencys(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.user_type != 'patient':
        return redirect('/home/')

    Emergency_requests = EmergencyRequest.objects.filter(sender=request.user)

    return render(request, 'my_Emergencys.html', {'Emergency_requests': Emergency_requests})

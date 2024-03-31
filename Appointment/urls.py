from django.urls import path
from . import views

urlpatterns = [
    path('send-appointment-request/', views.send_appointment_request, name='send_appointment_request'),
    path('accept-appointment-request/<int:appointment_request_id>/', views.accept_appointment_request, name='accept_appointment_request'),
    path('decline-appointment-request/<int:appointment_request_id>/', views.decline_appointment_request, name='decline_appointment_request'),
    path('appointment-requests/', views.appointment_requests_view, name='appointment_requests'),
    path('upcoming-appointments/', views.upcoming_appointments, name='upcoming_appointments'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]

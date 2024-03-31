from django.urls import path
from notification.views import ShowNotifications
from Appointment.views import appointment_requests_view
from Emergency.views import Emergency_requests_view

urlpatterns = [
    path('', ShowNotifications, name='show-notifications'),
    path('appointment-requests/',appointment_requests_view, name='appointment-requests'),

]
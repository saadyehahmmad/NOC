from django.urls import path
from . import views

urlpatterns = [
    path('send-Emergency-request/', views.send_Emergency_request, name='send_Emergency_request'),
    path('accept-Emergency-request/<int:Emergency_request_id>/', views.accept_Emergency_request, name='accept_Emergency_request'),
    path('decline-Emergency-request/<int:Emergency_request_id>/', views.decline_Emergency_request, name='decline_Emergency_request'),
    path('Emergency-requests/', views.Emergency_requests_view, name='Emergency_requests'),
    path('upcoming-Emergency/', views.upcoming_Emergency, name='upcoming_Emergency'),
    path('my-Emergencys/', views.my_Emergencys, name='my_Emergencys'),
    path('update_profile_status/', views.update_profile_status, name='update_profile_status'),

]

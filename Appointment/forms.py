# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import AppointmentRequest
from users.models import Profile  # Import the Profile model if user_type is stored there

class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        fields = ['receiver', 'location', 'services_needed','note', 'date_time_available']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user and user.profile.user_type == 'patient':  # Check if user is a nurse
            # Filter the choices for receiver based on user_type
            self.fields['receiver'].queryset = User.objects.filter(profile__user_type='nurse')
            # If user_type is stored in Profile model, modify the queryset accordingly
        else:
            # If user is not a nurse, show all users as choices for receiver
            self.fields['receiver'].queryset = User.objects.all()

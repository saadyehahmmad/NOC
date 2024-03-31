from django.db import models
from django.contrib.auth.models import User
from django.utils  import timezone

class AppointmentRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_appointment_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_appointment_requests')
    location = models.CharField(max_length=100)
    services_needed = models.TextField()
    note = models.TextField(default="Nothing")
    date_time_available = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)  # New field to track acceptance
    timestamp = models.DateTimeField(auto_now_add=True)


    def accept(self):
        # Create an appointment when the request is accepted
        Appointment.objects.create(
            patient=self.sender,
            nurse=self.receiver,
            location=self.location,
            services_needed=self.services_needed,
            date_time=self.date_time_available,
            note = self.note,
            timestamp=self.timestamp,
        )
        # Deactivate the appointment request
        self.is_active = False
        self.is_accepted = True  # Mark the request as accepted
        self.save()

    def decline(self):
        self.is_active = False
        self.is_accepted = False  # Mark the request as accepted
        self.save()


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nurse_appointments')
    location = models.CharField(max_length=100)
    services_needed = models.TextField()
    note = models.TextField(default="Nothing")
    date_time = models.DateTimeField()
    timestamp = models.DateTimeField(null =True)



    def __str__(self):
        return f"Appointment for {self.patient.username} at {self.location} on {self.date_time} by {self.patient}"

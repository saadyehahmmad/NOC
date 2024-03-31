from django.db import models
from django.contrib.auth.models import User
from django.utils  import timezone

class EmergencyRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emergency_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emergency_requests')
    location = models.CharField(max_length=100)
    note = models.TextField(default="Nothing")
    is_active = models.BooleanField(default=True)
    is_accepted = models.BooleanField(default=False)  # New field to track acceptance
    timestamp = models.DateTimeField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    distance = models.FloatField(null=True)


    def accept(self):
        # Create an emergency when the request is accepted
        Emergency.objects.create(
            patient=self.sender,
            nurse=self.receiver,
            location=self.location,
            note = self.note,
            timestamp=self.timestamp,
        )
        # Deactivate the emergency request
        self.is_active = False
        self.is_accepted = True  # Mark the request as accepted
        self.save()

    def decline(self):
        self.is_active = False
        self.is_accepted = False  # Mark the request as accepted
        self.save()


class Emergency(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_emergencys')
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nurse_emergencys')
    location = models.CharField(max_length=100)
    note = models.TextField(default="Nothing")
    timestamp = models.DateTimeField(null =True)
    distance = models.FloatField(null=True)



    def __str__(self):
        return f"Emergency for {self.patient.username} at {self.location}  by {self.patient}"

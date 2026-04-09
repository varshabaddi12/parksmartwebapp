from django.db import models

class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=10)
    slot_type = models.CharField(max_length=20) # e.g., 2-wheeler, 4-wheeler
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.slot_number

class Booking(models.Model):
    full_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)
    slot_number = models.CharField(max_length=10)
    duration = models.IntegerField() # hours
    total_amount = models.IntegerField()
    # THIS LINE FIXES THE DASHBOARD ERROR:
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.full_name} - {self.slot_number}"
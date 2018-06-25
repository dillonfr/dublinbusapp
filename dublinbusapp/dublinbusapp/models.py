from django.db import models

class Bus(models.Model):
    bus_id = models.CharField(max_length=10)
    route = models.CharField(max_length=10)
    journey_time = models.CharField(max_length=100)
    bus_logo = models.CharField(max_length=1000)

    def __str__(self):
        return self.bus_id + ' - ' + self.route

class Passenger(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=5)

from django.db import models

# Create your models here.
class EVChargingLocation(models.Model):
    staionName = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.staionName
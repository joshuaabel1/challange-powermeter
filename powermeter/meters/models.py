from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Meter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    reading_datetime = models.DateTimeField(default=timezone.now)
    consumption = models.FloatField()

    def __str__(self):
        return str(self.meter_id)

    def clean(self):
        if self.consumption <= 0:
            raise ValidationError({'consumption': ('Consumption must be greater than zero.')})

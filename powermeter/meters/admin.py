from django.contrib import admin
from .models import Meter
from .models import Measurement
# Register your models here.


admin.site.register(Meter)
admin.site.register(Measurement)
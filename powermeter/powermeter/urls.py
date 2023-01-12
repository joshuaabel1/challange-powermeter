from django.contrib import admin
from django.urls import path
from meters.views import MeterCreateAPIView, MeasurementCreateAPIView, MaxMeasurementAPIView, MinMeasurementAPIView, AverageConsumptionAPIView, TotalConsumptionAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meter/', MeterCreateAPIView.as_view(), name='meter_create'),
    path('measurement/', MeasurementCreateAPIView.as_view(),
         name='measurement_create'),
    path('measurement/<int:id>/max/',
         MaxMeasurementAPIView.as_view(), name='max_measurement'),
    path('measurement/<int:id>/min/',
         MinMeasurementAPIView.as_view(), name='min_measurement'),
    path('measurement/<int:id>/average_consumption/',
         AverageConsumptionAPIView.as_view(), name='average_consumption'),
    path('meters/<int:id>/total_consumption/',
         TotalConsumptionAPIView.as_view(), name='total_consumption'),
]

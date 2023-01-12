from rest_framework import serializers
from .models import Meter
from .models import Measurement


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = ('id','name')


class MeasurementSerializer(serializers.ModelSerializer):
    def validate(self, data):
        meter_id = data['meter'].id
        try:
            meter = Meter.objects.get(id=meter_id)
        except Meter.DoesNotExist:
            raise serializers.ValidationError("Meter does not exist.")
        return data

    class Meta:
        model = Measurement
        fields = ('meter','reading_datetime','consumption')
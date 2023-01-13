from rest_framework.generics import CreateAPIView
from .models import Meter
from .serializer import MeterSerializer
from .models import Measurement
from .serializer import MeasurementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import Avg
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import serializers


class MeterCreateAPIView(CreateAPIView):
    queryset = Meter.objects.all()
    serializer_class = MeterSerializer
    permission_classes = [AllowAny]


class MeasurementCreateAPIView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.validated_data['consumption'] <= 0:
            raise serializers.ValidationError(
                {'consumption': 'Consumption must be greater than zero.'})
        serializer.save()


class MaxMeasurementAPIView(APIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        return self.queryset.filter(meter_id=self.kwargs.get('id'))

    def get(self, request, id):
        if not Meter.objects.filter(id=id).exists():
            return Response({"error": "Meter does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if not self.get_queryset().exists():
            return Response({"error": "Measurements for this meter does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        max_measurement = self.get_queryset().latest('consumption')
        serializer = MeasurementSerializer(max_measurement)
        return Response(serializer.data)


class MinMeasurementAPIView(APIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        return self.queryset.filter(meter_id=self.kwargs.get('id'))

    def get(self, request, id):
        if not Meter.objects.filter(id=id).exists():
            return Response({"error": "Meter does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if not self.get_queryset().exists():
            return Response({"error": "Measurements for this meter does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        min_measurement = self.get_queryset().earliest('consumption')
        serializer = MeasurementSerializer(min_measurement)
        return Response(serializer.data)


class TotalConsumptionAPIView(APIView):
    def get_queryset(self):
        return Measurement.objects.filter(meter_id=self.kwargs.get('id'))

    def get(self, request, id):
        queryset = self.get_queryset()
        try:
            meter = Meter.objects.get(id=id)
            if not queryset.exists():
                return Response({"error": "Meter does not exist or has no measurements."},
                                status=status.HTTP_404_NOT_FOUND)
            total_consumption = queryset.aggregate(
                sum_of_consumption=Sum('consumption'))
            return Response(total_consumption)
        except Meter.DoesNotExist:
            return Response({"error": "Meter does not exist."}, status=status.HTTP_404_NOT_FOUND)


class AverageConsumptionAPIView(APIView):
    queryset = Measurement.objects.all()

    def get_queryset(self):
        return self.queryset.filter(meter_id=self.kwargs.get('id'))

    def get(self, request, id):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"error": "Measurements for this meter do not exist."},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            meter = Meter.objects.get(id=id)
            average_consumption = meter.measurement_set.aggregate(
                avg_of_consumption=Avg('consumption'))
            return Response(average_consumption)
        except Meter.DoesNotExist:
            return Response({"error": "Meter does not exist."}, status=status.HTTP_404_NOT_FOUND)

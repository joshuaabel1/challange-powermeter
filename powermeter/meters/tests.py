from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Meter, Measurement
from .serializer import MeasurementSerializer
import json


class AverageConsumptionAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.meter = Meter.objects.create(name='test')
        self.measurement1 = Measurement.objects.create(meter=self.meter, consumption=10)
        self.measurement2 = Measurement.objects.create(meter=self.meter, consumption=20)
        self.measurement3 = Measurement.objects.create(meter=self.meter, consumption=30)

    def test_valid_average_consumption(self):
        response = self.client.get(reverse('average_consumption', kwargs={'id': self.meter.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'avg_of_consumption': 20.0})

    def test_invalid_average_consumption(self):
        response = self.client.get(reverse('average_consumption', kwargs={'id': 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Measurements for this meter do not exist.'})


class MinMeasurementAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.meter1 = Meter.objects.create(name='Meter 1')
        self.measurement1 = Measurement.objects.create(meter=self.meter1, consumption=1)
        self.measurement2 = Measurement.objects.create(meter=self.meter1, consumption=2)
        self.measurement3 = Measurement.objects.create(meter=self.meter1, consumption=3)

    def test_valid_min_measurement(self):
        response = self.client.get(reverse('min_measurement', kwargs={'id': self.meter1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MeasurementSerializer(self.measurement1).data)

    def test_min_measurement_not_exist(self):
        response = self.client.get(reverse('min_measurement', kwargs={'id': 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Meter does not exist.'})
        
    def test_measurement_not_exist(self):
        non_existing_meter = Meter.objects.create(name='Non-existing meter')
        response = self.client.get(reverse('min_measurement', kwargs={'id': non_existing_meter.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Measurements for this meter does not exist.'})


class MaxMeasurementAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.meter = Meter.objects.create(id=1)
        self.measurement1 = Measurement.objects.create(meter=self.meter, consumption=5)
        self.measurement2 = Measurement.objects.create(meter=self.meter, consumption=10)
        self.measurement3 = Measurement.objects.create(meter=self.meter, consumption=15)

    def test_valid_max_measurement(self):
        response = self.client.get(reverse('max_measurement', kwargs={'id': self.meter.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['consumption'], 15)

    def test_invalid_max_measurement(self):
        response = self.client.get(reverse('max_measurement', kwargs={'id': 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Meter does not exist.')

    
class MeasurementCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.meter = Meter.objects.create(name='test')
        self.valid_payload = {
            'meter': self.meter.id,
            'consumption': 5,
        }
        self.invalid_payload = {
            'meter': self.meter.id,
            'consumption': 0,
            'reading_datetime': '2022-01-01T00:00:00Z'
        }

    def test_create_valid_measurement(self):
        response = self.client.post(
            reverse('measurement_create'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Measurement.objects.get().consumption, 5)
        self.assertEqual(Measurement.objects.get().meter.id, self.meter.id)

    def test_create_invalid_measurement(self):
        response = self.client.post(
            reverse('measurement_create'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Measurement.objects.count(), 0)

class MeterCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {'id':1,'name': 'Meter 1'}
        self.invalid_payload = {'name': ''}

    def test_create_valid_meter(self):
        response = self.client.post(
            reverse('meter_create'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meter.objects.count(), 1)
        self.assertEqual(Meter.objects.get().name, 'Meter 1')

    def test_create_invalid_meter(self):
        response = self.client.post(
            reverse('meter_create'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TotalConsumptionAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.meter = Meter.objects.create(id=1)
        self.valid_payload = {
            'meter': self.meter.id,
            'consumption': 1,
        }
        self.invalid_payload = {
            'meter': 99,
            'consumption': '',
        }

    def test_valid_total_consumption(self):
        self.client.post(
            reverse('measurement_create'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.client.post(
            reverse('measurement_create'),
            data=json.dumps({'meter': self.meter.id, 'consumption': 2}),
            content_type='application/json'
        )
        response = self.client.get(reverse('total_consumption', kwargs={'id': self.meter.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'sum_of_consumption': 3})

    def test_invalid_total_consumption(self):
        response = self.client.get(reverse('total_consumption', kwargs={'id': 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Meter does not exist.'})
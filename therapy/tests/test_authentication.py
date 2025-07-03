from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import GeneralUser as User
from therapy.models import (
    RadiationTherapyType,
    Location,
    SpecLocation,
    Diagnosis,
    ClinicalCase,
    Unit,
    Parameter,
    ModelName,
    Stage,
    RiskGroup,
    Complication,
    ModelStructure,
    Result,
    Source,
    DataSet,
    Histology,
    Grade, 
    Tumor, 
    Node, 
    Metastasis,
    ClinicalCaseComplication 
)

class AuthenticationTest(APITestCase):
    def test_unauthenticated_access(self):
        endpoints = [
            reverse('radiation-therapy-type-list'),
            reverse('сlinical-сase-сomplication-list'),
            reverse('location-list'),
            reverse('spec-location-list'),
            reverse('diagnosis-list'),
            reverse('clinical-case-list'),
            reverse('result-list'),
            reverse('aggregate-metrics-list')
        ]
        
        for url in endpoints:
            if url == reverse('aggregate-metrics-list'):
                response = self.client.post(url, {})
            else:
                response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        
        url = reverse('location-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PermissionTest(APITestCase):
    def test_write_permissions(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        
        # Complication has IsAuthenticatedOrReadOnly permission
        url = reverse('complication-list')
        
        # GET should be allowed
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # POST should be allowed for authenticated users
        loc = Location.objects.create(name='Test Location', short_name='TL')
        spec_loc = SpecLocation.objects.create(location=loc, name='Test Spec Location')
        data = {'name': 'New Complication', 'spec_location': spec_loc.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
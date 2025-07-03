from django.test import TestCase
from therapy.models import ClinicalCase, SpecLocation, Location, RadiationTherapyType

class ClinicalCaseModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Общая локализация")
        self.spec_location = SpecLocation.objects.create(name="Тестовая локализация", location=self.location)
        self.therapy_type = RadiationTherapyType.objects.create(name="Фотонная")

    def test_create_clinical_case(self):
        case = ClinicalCase.objects.create(
            quantity=1,
            spec_location=self.spec_location,
            radiation_therapy_type=self.therapy_type
        )
        self.assertEqual(case.quantity, 1)
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




class RadiationTherapyTypeViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.rt_type = RadiationTherapyType.objects.create(name='Test RT Type', note='Note')
        self.url = reverse('radiation-therapy-type-list')

    def test_list_rt_types(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_rt_type(self):
        data = {'name': 'New RT Type', 'note': 'New note'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RadiationTherapyType.objects.count(), 2)

class ClinicalCaseComplicationViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create necessary dependencies
        loc = Location.objects.create(name='Test Location', short_name='TL')
        spec_loc = SpecLocation.objects.create(location=loc, name='Test Spec Location')
        complication = Complication.objects.create(name='Test Complication', spec_location=spec_loc)
        diagnosis = Diagnosis.objects.create(code='C00', description='Test Diagnosis')
        rt_type = RadiationTherapyType.objects.create(name='Test RT Type')
        
        self.case = ClinicalCase.objects.create(
            spec_location=spec_loc,
            diagnosis=diagnosis,
            gender=1,
            age=50,
            radiation_therapy_type=rt_type,
        )
        self.complication_link = ClinicalCaseComplication.objects.create(
            clinical_case=self.case,
            complication=complication
        )
        self.url = reverse('сlinical-сase-сomplication-list')

    def test_list_complications(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class LocationViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.location = Location.objects.create(name='Test Location', short_name='TL', note='Note')
        self.url = reverse('location-list')

    def test_list_locations(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Location')

    def test_search_locations(self):
        response = self.client.get(self.url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class SpecLocationViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.location = Location.objects.create(name='Test Location', short_name='TL')
        self.spec_location = SpecLocation.objects.create(location=self.location, name='Test Spec Location')
        self.url = reverse('spec-location-list')

    def test_list_spec_locations(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class DiagnosisViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.diagnosis = Diagnosis.objects.create(code='C00', description='Test Diagnosis', note='Note')
        self.url = reverse('diagnosis-list')

    def test_list_diagnoses(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ClinicalCaseViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create necessary objects
        loc = Location.objects.create(name='Test Location', short_name='TL')
        spec_loc = SpecLocation.objects.create(location=loc, name='Test Spec Location')
        diagnosis = Diagnosis.objects.create(code='C00', description='Test Diagnosis')
        complication = Complication.objects.create(name='Test Complication', spec_location=spec_loc)
        stage = Stage.objects.create(name='Test Stage')
        risk_group = RiskGroup.objects.create(name='Test Risk Group')
        rt_type = RadiationTherapyType.objects.create(name='Test RT Type')
        histology = Histology.objects.create(name='Test Histology')
        grade = Grade.objects.create(name='Test Grade')
        tumor = Tumor.objects.create(short_name='T', name='Test Tumor')
        node = Node.objects.create(short_name='N', name='Test Node')
        metastasis = Metastasis.objects.create(short_name='M', name='Test Metastasis')
        
        self.case1 = ClinicalCase.objects.create(
            spec_location=spec_loc,
            diagnosis=diagnosis,
            gender=1,
            age=45,
            stage=stage,
            risk_group=risk_group,
            radiation_therapy_type=rt_type,
            histology=histology,
            grade=grade,
            tumor=tumor,
            node=node,
            metastasis=metastasis,
            number_of_fractions=30,
            single_dose=2.0,
            treatment_duration=45
        )
        
        self.case2 = ClinicalCase.objects.create(
            spec_location=spec_loc,
            diagnosis=diagnosis,
            gender=1,
            age=55,
            number_of_fractions=25,
            radiation_therapy_type=rt_type,
        )
        
        ClinicalCaseComplication.objects.create(
            clinical_case=self.case1,
            complication=complication
        )
        
        self.url = reverse('clinical-case-list')

    def test_list_cases(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_location(self):
        location_id = Location.objects.first().id
        response = self.client.get(self.url, {'location': location_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_age(self):
        response = self.client.get(self.url, {'age': 45})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['age'], 45)

    def test_filter_by_gender(self):
        response = self.client.get(self.url, {'gender': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_complication(self):
        complication_id = Complication.objects.first().id
        response = self.client.get(self.url, {'complication': complication_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_multiple_params(self):
        response = self.client.get(self.url, {
            'gender':1,
            'number_of_fractions': 30
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ResultViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create clinical case
        loc = Location.objects.create(name='Test Location', short_name='TL')
        spec_loc = SpecLocation.objects.create(location=loc, name='Test Spec Location')
        diagnosis = Diagnosis.objects.create(code='C00', description='Test Diagnosis')
        rt_type = RadiationTherapyType.objects.create(name='Test RT Type')
        self.case = ClinicalCase.objects.create(
            spec_location=spec_loc,
            diagnosis=diagnosis,
            gender=1,
            age=50,
            radiation_therapy_type=rt_type,
        )
        
        # Create model structure
        unit = Unit.objects.create(name='Gy', full_name='Gray')
        parameter = Parameter.objects.create(name='Dose', full_name='Total Dose', unit=unit)
        model_name = ModelName.objects.create(name='NTCP Model', full_name='NTCP Model Full', model_type=2)
        model_structure = ModelStructure.objects.create(model_name=model_name, parameter=parameter)
        
        # Create dataset and result
        source = Source.objects.create(name='Test Source')
        dataset = DataSet.objects.create(clinical_case=self.case, source=source)
        self.result = Result.objects.create(
            data_set=dataset,
            model_structure=model_structure,
            value=10.5
        )
        
        self.url = reverse('result-list')

    def test_list_results(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_clinical_case(self):
        response = self.client.get(self.url, {'clinical_case': self.case.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['value']), 10.5)

class DataSetViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create clinical case
        loc = Location.objects.create(name='Test Location', short_name='TL')
        spec_loc = SpecLocation.objects.create(location=loc, name='Test Spec Location')
        diagnosis = Diagnosis.objects.create(code='C00', description='Test Diagnosis')
        rt_type = RadiationTherapyType.objects.create(name='Test RT Type')
        case = ClinicalCase.objects.create(
            spec_location=spec_loc,
            diagnosis=diagnosis,
            gender=1,
            age=50,
            radiation_therapy_type=rt_type,
        )
        
        # Create dataset
        source = Source.objects.create(name='Test Source')
        self.dataset = DataSet.objects.create(clinical_case=case, source=source)
        
        self.url = reverse('dataset-list')

    def test_list_datasets(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class AggregatedMetricsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create clinical cases
        loc = Location.objects.create(name='Test Location', short_name='TL')
        spec_loc = SpecLocation.objects.create(location=loc, name='Test Spec Location')
        diagnosis = Diagnosis.objects.create(code='C00', description='Test Diagnosis')
        rt_type = RadiationTherapyType.objects.create(name='Test RT Type')
        
        self.case1 = ClinicalCase.objects.create(
            spec_location=spec_loc,
            diagnosis=diagnosis,
            gender=1,
            age=45,
            number_of_fractions=30,
            single_dose=2.0,
            treatment_duration=45,
            radiation_therapy_type=rt_type,
        )
        
        self.case2 = ClinicalCase.objects.create(
            spec_location=spec_loc,
            diagnosis=diagnosis,
            gender=2,
            age=55,
            number_of_fractions=25,
            single_dose=1.8,
            treatment_duration=35,
            radiation_therapy_type=rt_type,
        )
        
        # Create model structure
        unit = Unit.objects.create(name='Gy', full_name='Gray')
        parameter = Parameter.objects.create(name='Dose', full_name='Total Dose', unit=unit)
        model_name = ModelName.objects.create(name='NTCP Model', full_name='NTCP Model Full', model_type=2)
        model_structure = ModelStructure.objects.create(model_name=model_name, parameter=parameter)
        
        # Create datasets and results
        source = Source.objects.create(name='Test Source')
        
        dataset1 = DataSet.objects.create(clinical_case=self.case1, source=source)
        Result.objects.create(data_set=dataset1, model_structure=model_structure, value=10.0)
        Result.objects.create(data_set=dataset1, model_structure=model_structure, value=20.0)
        
        dataset2 = DataSet.objects.create(clinical_case=self.case2, source=source)
        Result.objects.create(data_set=dataset2, model_structure=model_structure, value=15.0)
        
        self.url = reverse('aggregate-metrics-list')

    def test_aggregation(self):
        data = {
            "clinical_case_ids": [self.case1.id, self.case2.id]
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        
        self.assertEqual(response_data['clinical_case_count'], 2)
        self.assertEqual(response_data['result_count'], 3)
        
        aggregated_params = response_data['aggregated_parameters']
        self.assertEqual(len(aggregated_params), 1)
        
        param_data = aggregated_params[0]
        self.assertEqual(param_data['parameter'], 'Dose')
        self.assertEqual(param_data['unit'], 'Gy')
        self.assertEqual(param_data['count'], 3)
        self.assertEqual(param_data['average'], 15.0)
        self.assertEqual(param_data['min_value'], 10.0)
        self.assertEqual(param_data['max_value'], 20.0)
        
        # Verify min meta
        self.assertEqual(param_data['min_meta']['number_of_fractions'], 30)
        self.assertEqual(param_data['min_meta']['single_dose'], 2.0)
        self.assertEqual(param_data['min_meta']['treatment_duration'], 45)
        self.assertEqual(param_data['min_meta']['clinical_case_id'], self.case1.id)
        
        # Verify max meta
        self.assertEqual(param_data['max_meta']['number_of_fractions'], 30)
        self.assertEqual(param_data['max_meta']['single_dose'], 2.0)
        self.assertEqual(param_data['max_meta']['treatment_duration'], 45)
        self.assertEqual(param_data['max_meta']['clinical_case_id'], self.case1.id)


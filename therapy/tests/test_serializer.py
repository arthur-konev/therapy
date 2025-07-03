from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import serializers  

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
from therapy.serializers import (
    LocationSerializer,
    SpecLocationSerializer,
    DiagnosisSerializer,
    ClinicalCaseSerializer,
    UnitSerializer,
    ParameterSerializer,
    ModelNameSerializer,
    StageSerializer,
    RiskGroupSerializer,
    ComplicationSerializer,
    ModelStructureSerializer,
    ResultSerializer,
    SourceSerializer,
    DataSetSerializer,
    RadiationTherapyTypeSerializer,
    HistologySerializer,
    GradeSerializer,
    TumorSerializer,
    NodeSerializer,
    MetastasisSerializer,
    ClinicalCaseComplicationSerializer,
)



class RadiationTherapyTypeSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Брахитерапия",
            "note": "Внутреннее облучение"
        }
        self.instance = RadiationTherapyType.objects.create(**self.valid_data)
        self.serializer = RadiationTherapyTypeSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'note'})
    
    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.valid_data['name'])
    
    def test_note_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['note'], self.valid_data['note'])
    
    # def test_valid_deserialization(self):
    #     serializer = RadiationTherapyTypeSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.name, self.valid_data['name'])
    
    def test_invalid_deserialization_missing_name(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['name']
        serializer = RadiationTherapyTypeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
    
    def test_unique_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = RadiationTherapyTypeSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
 
class LocationSerializerTest(TestCase):
        def setUp(self):
            self.valid_data = {
                "name": "Голова",
                "short_name": "Head",
                "note": "Верхняя часть тела"
            }
            self.instance = Location.objects.create(**self.valid_data)
            self.serializer = LocationSerializer(instance=self.instance)
        
        def test_contains_expected_fields(self):
            data = self.serializer.data
            self.assertEqual(set(data.keys()), 
                            {'id', 'name', 'short_name', 'created_at', 'updated_at', 'note'})
        
        def test_name_field_content(self):
            data = self.serializer.data
            self.assertEqual(data['name'], self.valid_data['name'])
        
        def test_created_at_field(self):
            data = self.serializer.data
            self.assertIsNotNone(data['created_at'])
        
        # def test_valid_deserialization(self):
        #     serializer = LocationSerializer(data=self.valid_data)
        #     self.assertTrue(serializer.is_valid())
        #     obj = serializer.save()
        #     self.assertEqual(obj.name, self.valid_data['name'])
        
        def test_unique_name_validation(self):
            duplicate_data = self.valid_data.copy()
            serializer = LocationSerializer(data=duplicate_data)
            self.assertFalse(serializer.is_valid())
            self.assertIn('name', serializer.errors)
               
class SpecLocationSerializerTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Голова", short_name="Head")
        self.valid_data = {
            "name": "Теменная область",
            "location": self.location.id,
            "note": "Правая сторона"
        }
        self.instance = SpecLocation.objects.create(
            name=self.valid_data['name'],
            location=self.location,
            note=self.valid_data['note']
        )
        self.serializer = SpecLocationSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'location', 'note', 'name_location'})
    
    def test_name_location_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_location'], self.location.name)
    
    # def test_valid_deserialization(self):
    #     serializer = SpecLocationSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.name, self.valid_data['name'])
    #     self.assertEqual(obj.location, self.location)
    
    def test_location_required(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['location']
        serializer = SpecLocationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('location', serializer.errors)
        
class DiagnosisSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "code": "C50",
            "description": "Рак молочной железы",
            "note": "Злокачественное новообразование"
        }
        self.instance = Diagnosis.objects.create(**self.valid_data)
        self.serializer = DiagnosisSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'code', 'description', 'note'})
    
    def test_code_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['code'], self.valid_data['code'])
    
    # def test_valid_deserialization(self):
    #     serializer = DiagnosisSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.code, self.valid_data['code'])
    
    # def test_unique_code_validation(self):
    #     duplicate_data = self.valid_data.copy()
    #     serializer = DiagnosisSerializer(data=duplicate_data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('code', serializer.errors)
        
class StageSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "IIA",
            "note": "Опухоль до 5 см без поражения лимфоузлов"
        }
        self.instance = Stage.objects.create(**self.valid_data)
        self.serializer = StageSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'note'})
    
    def test_all_fields_optional(self):
        minimal_data = {}
        serializer = StageSerializer(data=minimal_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNone(obj.name)
    
    def test_valid_deserialization(self):
        serializer = StageSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.name, self.valid_data['name'])

class RiskGroupSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Высокий риск",
            "note": "Пациенты с множественными факторами риска"
        }
        self.instance = RiskGroup.objects.create(**self.valid_data)
        self.serializer = RiskGroupSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'note'})
    
    def test_all_fields_optional(self):
        minimal_data = {}
        serializer = RiskGroupSerializer(data=minimal_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNone(obj.name)
    
    def test_valid_deserialization(self):
        serializer = RiskGroupSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.name, self.valid_data['name'])

class ComplicationSerializerTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Кожа")
        self.spec_location = SpecLocation.objects.create(
            name="Эпидермис",
            location=self.location
        )
        
        self.valid_data = {
            "name": "Дерматит",
            "alt_name": "Радиационный дерматит",
            "spec_location": self.spec_location.id,
            "note": "Покраснение кожи"
        }
        
        self.instance = Complication.objects.create(
            name=self.valid_data['name'],
            alt_name=self.valid_data['alt_name'],
            spec_location=self.spec_location,
            note=self.valid_data['note']
        )
        self.serializer = ComplicationSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), 
                         {'id', 'name', 'alt_name', 'spec_location', 'name_location', 'note'})
    
    def test_name_location_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_location'], self.spec_location.name)
    
    # def test_valid_deserialization(self):
    #     serializer = ComplicationSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.name, self.valid_data['name'])
    
    def test_unique_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = ComplicationSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        
class HistologySerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Аденокарцинома",
            "note": "Злокачественная опухоль железистого эпителия"
        }
        self.instance = Histology.objects.create(**self.valid_data)
        self.serializer = HistologySerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'note'})
    
    # def test_valid_deserialization(self):
    #     serializer = HistologySerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.name, self.valid_data['name'])
    
    def test_unique_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = HistologySerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        

class GradeSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "G2",
            "note": "Умеренно дифференцированная опухоль"
        }
        self.instance = Grade.objects.create(**self.valid_data)
        self.serializer = GradeSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'note'})
    
    # def test_valid_deserialization(self):
    #     serializer = GradeSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.name, self.valid_data['name'])
    
    def test_unique_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = GradeSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

class TumorSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "short_name": "T2",
            "name": "Опухоль размером 2-5 см",
            "note": "Без инвазии окружающих тканей"
        }
        self.instance = Tumor.objects.create(**self.valid_data)
        self.serializer = TumorSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'short_name', 'name', 'note'})
    
    # def test_valid_deserialization(self):
    #     serializer = TumorSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.short_name, self.valid_data['short_name'])
    
    def test_unique_short_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = TumorSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('short_name', serializer.errors)
        
class NodeSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "short_name": "N1",
            "name": "Метастазы в регионарных лимфоузлах",
            "note": "На стороне первичной опухоли"
        }
        self.instance = Node.objects.create(**self.valid_data)
        self.serializer = NodeSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'short_name', 'name', 'note'})
    
    # def test_valid_deserialization(self):
    #     serializer = NodeSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.short_name, self.valid_data['short_name'])
    
    def test_unique_short_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = NodeSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('short_name', serializer.errors)
        
class MetastasisSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "short_name": "M1",
            "name": "Отдаленные метастазы",
            "note": "Включая поражение других органов"
        }
        self.instance = Metastasis.objects.create(**self.valid_data)
        self.serializer = MetastasisSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'short_name', 'name', 'note'})
    
    # def test_valid_deserialization(self):
    #     serializer = MetastasisSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.short_name, self.valid_data['short_name'])
    
    def test_unique_short_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = MetastasisSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('short_name', serializer.errors)       
        
class UnitSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Гр",
            "full_name": "Грей",
            "note": "Единица поглощенной дозы"
        }
        self.instance = Unit.objects.create(**self.valid_data)
        self.serializer = UnitSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'full_name', 'note'})
    
    # def test_valid_deserialization(self):
    #     serializer = UnitSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.name, self.valid_data['name'])
    
    def test_unique_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = UnitSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        
class ParameterSerializerTest(TestCase):
    def setUp(self):
        self.unit = Unit.objects.create(name="Гр")
        
        self.valid_data = {
            "name": "D50",
            "full_name": "Доза, дающая 50% эффекта",
            "unit": self.unit.id,
            "note": "Параметр модели"
        }
        
        self.instance = Parameter.objects.create(
            name=self.valid_data['name'],
            full_name=self.valid_data['full_name'],
            unit=self.unit,
            note=self.valid_data['note']
        )
        self.serializer = ParameterSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), 
                         {'id', 'name', 'full_name', 'unit', 'note', 'name_unit'})
    
    def test_name_unit_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_unit'], self.unit.name)
    
    def test_valid_deserialization(self):
        serializer = ParameterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.name, self.valid_data['name'])
        self.assertEqual(obj.unit, self.unit)
    
    def test_unit_optional(self):
        data_without_unit = self.valid_data.copy()
        del data_without_unit['unit']
        
        serializer = ParameterSerializer(data=data_without_unit)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNone(obj.unit)
        
class ModelNameSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "LQ",
            "full_name": "Линейно-квадратичная модель",
            "model_type": ModelName.ModelTypeChoises.TCP,
            "note": "Модель для расчета TCP"
        }
        self.instance = ModelName.objects.create(**self.valid_data)
        self.serializer = ModelNameSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'full_name', 'model_type', 'note'})
    
    def test_model_type_field(self):
        data = self.serializer.data
        self.assertEqual(data['model_type'], ModelName.ModelTypeChoises.TCP)
    
    # def test_valid_deserialization(self):
    #     serializer = ModelNameSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.name, self.valid_data['name'])
    
    def test_unique_name_validation(self):
        duplicate_data = self.valid_data.copy()
        serializer = ModelNameSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        
class SourceSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "PMID:12345678",
            "full_name": "Journal of Radiation Oncology, 2023",
            "url": "https://example.com/article",
            "note": "Основной источник данных"
        }
        self.instance = Source.objects.create(**self.valid_data)
        self.serializer = SourceSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'full_name', 'url', 'note'})
    
    def test_valid_url(self):
        data = self.serializer.data
        self.assertEqual(data['url'], self.valid_data['url'])
    
    def test_valid_deserialization(self):
        serializer = SourceSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.name, self.valid_data['name'])
    
    def test_url_optional(self):
        data_without_url = self.valid_data.copy()
        del data_without_url['url']
        
        serializer = SourceSerializer(data=data_without_url)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNone(obj.url)
        
class DataSetSerializerTest(TestCase):
    def setUp(self):
        # Создаем зависимости
        self.case = ClinicalCase.objects.create(
            spec_location=SpecLocation.objects.create(
                name="Локализация",
                location=Location.objects.create(name="Базовая локализация")
            ),
            radiation_therapy_type=RadiationTherapyType.objects.create(
                name="Тип терапии"
            )
        )
        self.source = Source.objects.create(name="Источник 1", url="https://example.com")
        
        self.valid_data = {
            "clinical_case": self.case.id,
            "source": self.source.id,
            "note": "Набор данных для анализа"
        }
        
        self.instance = DataSet.objects.create(
            clinical_case=self.case,
            source=self.source,
            note=self.valid_data['note']
        )
        self.serializer = DataSetSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), 
                         {'id', 'clinical_case', 'name_clinical_case', 
                          'source', 'note', 'name_source', 'url_source'})
    
    def test_name_clinical_case_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_clinical_case'], str(self.case))
    
    def test_name_source_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_source'], self.source.name)
    
    def test_url_source_field(self):
        data = self.serializer.data
        self.assertEqual(data['url_source'], self.source.url)
    
    def test_valid_deserialization(self):
        serializer = DataSetSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.clinical_case, self.case)
        self.assertEqual(obj.source, self.source)
    
    def test_all_fields_optional(self):
        minimal_data = {}
        serializer = DataSetSerializer(data=minimal_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNone(obj.clinical_case)
        self.assertIsNone(obj.source)        
        
class ClinicalCaseSerializerTest(APITestCase):
    def setUp(self):
        # Создаем все зависимости
        self.diagnosis = Diagnosis.objects.create(
            code="C50", 
            description="Рак молочной железы"
        )
        self.location = Location.objects.create(name="Грудь")
        self.spec_location = SpecLocation.objects.create(
            name="Молочная железа", 
            location=self.location
        )
        self.therapy_type = RadiationTherapyType.objects.create(
            name="Внешнее облучение"
        )
        
        self.valid_data = {
            "age": 45,
            "quantity": 3,
            "gender": 2,  # Женский
            "diagnosis": self.diagnosis.id,
            "refined_diagnosis": "Инвазивная карцинома",
            "spec_location": self.spec_location.id,
            "radiation_therapy_type": self.therapy_type.id,
            "number_of_fractions": 25,
            "single_dose": 2.0,
            "treatment_duration": 35
        }
        
        self.instance = ClinicalCase.objects.create(
            age=self.valid_data['age'],
            quantity=self.valid_data['quantity'],
            gender=self.valid_data['gender'],
            diagnosis=self.diagnosis,
            refined_diagnosis=self.valid_data['refined_diagnosis'],
            spec_location=self.spec_location,
            radiation_therapy_type=self.therapy_type,
            number_of_fractions=self.valid_data['number_of_fractions'],
            single_dose=self.valid_data['single_dose'],
            treatment_duration=self.valid_data['treatment_duration']
        )
        self.serializer = ClinicalCaseSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {
            'id', 'age', 'age_min', 'age_max', 'quantity', 'gender', 'diagnosis',
            'refined_diagnosis', 'spec_location', 'stage', 'risk_group', 
            'radiation_therapy_type', 'number_of_fractions', 'single_dose',
            'treatment_duration', 'histology', 'grade', 'tumor', 'node',
            'metastasis', 'note', 'name_location', 'name_diagnosis', 
            'name_stage', 'name_risk_group', 'name_radiation_therapy_type',
            'name_tumor', 'name_node', 'name_metastasis', 'name_histology',
            'name_grade', 'gender_display', 'clinical_case_text', 'text_location',
            'text_diagnosis', 'text_stage', 'text_risk_group', 
            'text_radiation_therapy_type', 'text_tumor', 'text_node',
            'text_metastasis', 'text_histology', 'text_grade',
            'datasets_source_name', 'datasets_source_url', 'datasets_result',
            'complications'
        }
        self.assertEqual(set(data.keys()), expected_fields)
    
    def test_name_location_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_location'], self.spec_location.name)
    
    def test_name_diagnosis_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_diagnosis'], self.diagnosis.code)
    
    def test_gender_display_field(self):
        data = self.serializer.data
        self.assertEqual(data['gender_display'], "Женский")
    
    def test_text_location_field(self):
        data = self.serializer.data
        self.assertEqual(data['text_location'], str(self.spec_location))
    
    def test_valid_deserialization(self):
        serializer = ClinicalCaseSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.age, self.valid_data['age'])
        self.assertEqual(obj.quantity, self.valid_data['quantity'])
    
    def test_required_fields(self):
        # spec_location и radiation_therapy_type обязательны
        invalid_data = self.valid_data.copy()
        del invalid_data['spec_location']
        del invalid_data['radiation_therapy_type']
        
        serializer = ClinicalCaseSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('spec_location', serializer.errors)
        self.assertIn('radiation_therapy_type', serializer.errors)
    
    def test_default_quantity(self):
        data_without_quantity = self.valid_data.copy()
        del data_without_quantity['quantity']
        
        serializer = ClinicalCaseSerializer(data=data_without_quantity)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.quantity, 1)  # Проверка значения по умолчанию
        
class ModelStructureSerializerTest(TestCase):
    def setUp(self):
        self.unit = Unit.objects.create(name="Гр", full_name="Грей")
        self.parameter = Parameter.objects.create(
            name="α/β", 
            unit=self.unit,
            note="Параметр модели LQ"
        )
        self.model_name = ModelName.objects.create(
            name="LQ",
            model_type=ModelName.ModelTypeChoises.TCP
        )
        
        self.valid_data = {
            "model_name": self.model_name.id,
            "parameter": self.parameter.id,
            "note": "Основная структура"
        }
        
        self.instance = ModelStructure.objects.create(
            model_name=self.model_name,
            parameter=self.parameter,
            note=self.valid_data['note']
        )
        self.serializer = ModelStructureSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), 
                         {'id', 'model_name', 'parameter', 'note', 
                          'name_model_name', 'name_parameter', 'name_unit'})
    
    def test_name_model_name_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_model_name'], self.model_name.name)
    
    def test_name_parameter_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_parameter'], self.parameter.name)
    
    def test_name_unit_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_unit'], self.unit.name)
    
    def test_valid_deserialization(self):
        serializer = ModelStructureSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.model_name, self.model_name)
        self.assertEqual(obj.parameter, self.parameter)

class ResultSerializerTest(TestCase):
    def setUp(self):
        # Создаем сложные зависимости
        self.unit = Unit.objects.create(name="Гр")
        self.parameter = Parameter.objects.create(name="α", unit=self.unit)
        self.model_name = ModelName.objects.create(name="LQ")
        self.model_structure = ModelStructure.objects.create(
            model_name=self.model_name,
            parameter=self.parameter
        )
        self.source = Source.objects.create(name="Источник 1", url="https://example.com")
        self.dataset = DataSet.objects.create(source=self.source)
        
        self.valid_data = {
            "model_structure": self.model_structure.id,
            "value": 0.35,
            "upper_value": 0.40,
            "lower_value": 0.30,
            "note": "Результат расчета",
            "data_set": self.dataset.id
        }
        
        self.instance = Result.objects.create(
            model_structure=self.model_structure,
            value=self.valid_data['value'],
            upper_value=self.valid_data['upper_value'],
            lower_value=self.valid_data['lower_value'],
            note=self.valid_data['note'],
            data_set=self.dataset
        )
        self.serializer = ResultSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {
            'id', 'model_structure', 'value', 'upper_value', 'lower_value', 
            'note', 'name_model_structure', 'name_parameter', 'name_unit', 
            'data_set', 'name_data_set'
        }
        self.assertEqual(set(data.keys()), expected_fields)
    
    # def test_name_model_structure_field(self):
    #     data = self.serializer.data
    #     self.assertEqual(data['name_model_structure'], self.model_name.name)
    
    def test_name_parameter_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_parameter'], self.parameter.name)
    
    def test_name_unit_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_unit'], self.unit.name)
    
    def test_name_data_set_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_data_set'], self.source.name)
    
    # def test_valid_deserialization(self):
    #     serializer = ResultSerializer(data=self.valid_data)
    #     self.assertTrue(serializer.is_valid())
    #     obj = serializer.save()
    #     self.assertEqual(obj.value, self.valid_data['value'])
    #     self.assertEqual(obj.data_set, self.dataset)
        
class ClinicalCaseComplicationSerializerTest(TestCase):
    def setUp(self):
        self.case = ClinicalCase.objects.create(
            # Минимальные обязательные поля
            spec_location=SpecLocation.objects.create(
                name="Локализация",
                location=Location.objects.create(name="Базовая локализация")
            ),
            radiation_therapy_type=RadiationTherapyType.objects.create(
                name="Тип терапии"
            )
        )
        self.complication = Complication.objects.create(
            name="Фиброз"
        )
        
        self.valid_data = {
            "clinical_case": self.case.id,
            "complication": self.complication.id
        }
        
        self.instance = ClinicalCaseComplication.objects.create(
            clinical_case=self.case,
            complication=self.complication
        )
        self.serializer = ClinicalCaseComplicationSerializer(instance=self.instance)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'clinical_case', 'complication', 'name_complication'})
    
    def test_name_complication_field(self):
        data = self.serializer.data
        self.assertEqual(data['name_complication'], self.complication.name)
    
    def test_valid_deserialization(self):
        serializer = ClinicalCaseComplicationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.clinical_case, self.case)
        self.assertEqual(obj.complication, self.complication)
        
        
        
        

from django.test import TestCase
from django.core.exceptions import ValidationError  

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

class RadiationTherapyTypeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.therapy = RadiationTherapyType.objects.create(
            name="Брахитерапия", 
            note="Внутреннее облучение"
        )

    def test_model_creation(self):
        """Тест создания объекта"""
        self.assertEqual(self.therapy.name, "Брахитерапия")
        self.assertEqual(self.therapy.note, "Внутреннее облучение")

    def test_name_uniqueness(self):
        """Тест уникальности поля name"""
        duplicate = RadiationTherapyType(name="Брахитерапия")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()  

    def test_string_representation(self):
        """Тест строкового представления"""
        self.assertEqual(
            str(self.therapy), 
            "Брахитерапия Внутреннее облучение"
        )

    def test_verbose_names(self):
        """Тест читаемых имен"""
        meta = RadiationTherapyType._meta
        self.assertEqual(meta.verbose_name, "Вид лучевой терапии")
        self.assertEqual(meta.verbose_name_plural, "Виды лучевой терапии")
        

class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые объекты
        cls.location = Location.objects.create(
            name="Голова",
            short_name="Head",
            note="Основная локализация"
        )
    
    def test_location_creation(self):
        """Тест создания объекта Location"""
        self.assertEqual(self.location.name, "Голова")
        self.assertEqual(self.location.short_name, "Head")
        self.assertEqual(self.location.note, "Основная локализация")
    
    def test_name_uniqueness(self):
        """Тест уникальности поля name"""
        duplicate = Location(name="Голова")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.location), "Голова (Head) Основная локализация")
    
    def test_verbose_names(self):
        """Тест метаданных модели"""
        meta = Location._meta
        self.assertEqual(meta.verbose_name, "Локализация")
        self.assertEqual(meta.verbose_name_plural, "Локализации")
    
    def test_auto_timestamps(self):
        """Тест автоматических временных меток"""
        self.assertIsNotNone(self.location.created_at)
        self.assertIsNotNone(self.location.updated_at)

class SpecLocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем родительскую локализацию
        cls.location = Location.objects.create(name="Голова")
        # Создаем уточненную локализацию
        cls.spec_location = SpecLocation.objects.create(
            name="Теменная область",
            location=cls.location,
            note="Правая сторона"
        )
    
    def test_speclocation_creation(self):
        """Тест создания объекта SpecLocation"""
        self.assertEqual(self.spec_location.name, "Теменная область")
        self.assertEqual(self.spec_location.location.name, "Голова")
        self.assertEqual(self.spec_location.note, "Правая сторона")
    
    def test_location_relationship(self):
        """Тест связи с Location"""
        self.assertEqual(self.location.speclocation_set.count(), 1)
        self.assertEqual(
            self.location.speclocation_set.first().name, 
            "Теменная область"
        )
    
    def test_cascade_delete(self):
        """Тест каскадного удаления"""
        location_id = self.location.id
        self.location.delete()
        
        # Проверяем что локализация удалена
        self.assertEqual(Location.objects.filter(id=location_id).count(), 0)
        # Проверяем что связанная уточненная локализация тоже удалена
        self.assertEqual(
            SpecLocation.objects.filter(id=self.spec_location.id).count(), 
            0
        )

class ClinicalCaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем необходимые связанные объекты
        cls.diagnosis = Diagnosis.objects.create(
            code="C50",
            description="Рак молочной железы"
        )
        
        cls.location = Location.objects.create(name="Грудь")
        cls.spec_location = SpecLocation.objects.create(
            name="Молочная железа",
            location=cls.location
        )
        
        cls.therapy_type = RadiationTherapyType.objects.create(
            name="Внешнее облучение"
        )
        
        # Создаем клинический случай с ВСЕМИ обязательными полями
        cls.case = ClinicalCase.objects.create(
            age=45,
            quantity=3,
            gender=ClinicalCase.GenderChoices.female,
            diagnosis=cls.diagnosis,
            refined_diagnosis="Инвазивная карцинома",
            spec_location=cls.spec_location,
            radiation_therapy_type=cls.therapy_type, 
            number_of_fractions=25,
            single_dose=2.0,
            treatment_duration=35
        )
    
    def test_clinical_case_creation(self):
        """Тест создания клинического случая"""
        self.assertEqual(self.case.radiation_therapy_type.name, "Внешнее облучение")
      
    
    def test_default_values(self):
        """Тест значений по умолчанию"""
        case = ClinicalCase.objects.create(
            spec_location=self.spec_location,
            radiation_therapy_type=self.therapy_type  
        )
        self.assertEqual(case.quantity, 1)
        self.assertEqual(case.gender, ClinicalCase.GenderChoices.INIT)
    
    def test_string_representation(self):
        """Тест сложного строкового представления"""
        str_repr = str(self.case)
        self.assertIn("Количество: 3", str_repr)
        self.assertIn("Возраст: 45", str_repr)
        self.assertIn("Пол: Женский", str_repr)
        self.assertIn("Диагноз: C50 - Рак молочной железы", str_repr)
        self.assertIn("Подробный диагноз: Инвазивная карцинома", str_repr)
        self.assertIn("Локализация: Молочная железа", str_repr)
        self.assertIn("Вид терапии: Внешнее облучение", str_repr)
        self.assertIn("Количество фракций: 25", str_repr)
        self.assertIn("Разовая доза: 2.0", str_repr)
        self.assertIn("Длительность лечения: 35 дней", str_repr)
    
    def test_optional_fields(self):
        """Тест необязательных полей"""
        case = ClinicalCase.objects.create(
            spec_location=self.spec_location,
            radiation_therapy_type=self.therapy_type
        )
        self.assertIsNone(case.age)
        self.assertIsNone(case.diagnosis)
        self.assertIsNone(case.refined_diagnosis)
    
    def test_foreign_key_relationships(self):
        """Тест связей ForeignKey"""
        self.assertEqual(
            self.diagnosis.clinicalcase_set.first(), 
            self.case
        )
        self.assertEqual(
            self.spec_location.clinicalcase_set.first(), 
            self.case
        )
        self.assertEqual(
            self.therapy_type.clinicalcase_set.first(), 
            self.case
        )
        
class DiagnosisModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnosis = Diagnosis.objects.create(
            code="C50",
            description="Рак молочной железы",
            note="Наиболее распространенный вид"
        )

    def test_diagnosis_creation(self):
        self.assertEqual(self.diagnosis.code, "C50")
        self.assertEqual(self.diagnosis.description, "Рак молочной железы")
        self.assertEqual(self.diagnosis.note, "Наиболее распространенный вид")
    
    def test_code_uniqueness(self):
        duplicate = Diagnosis(code="C50", description="Дубликат")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.diagnosis),
            "C50 - Рак молочной железы, Наиболее распространенный вид"
        )
    
    def test_verbose_names(self):
        meta = Diagnosis._meta
        self.assertEqual(meta.verbose_name, "Диагноз")
        self.assertEqual(meta.verbose_name_plural, "Диагнозы")
        
class StageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stage = Stage.objects.create(
            name="IIA",
            note="Опухоль до 5 см без поражения лимфоузлов"
        )

    def test_stage_creation(self):
        self.assertEqual(self.stage.name, "IIA")
        self.assertEqual(self.stage.note, "Опухоль до 5 см без поражения лимфоузлов")
    
    def test_optional_fields(self):
        stage = Stage.objects.create()
        self.assertIsNone(stage.name)
        self.assertIsNone(stage.note)
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.stage),
            "Стадия: IIA, Описание: Опухоль до 5 см без поражения лимфоузлов"
        ) 
        
class ComplicationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.location = Location.objects.create(name="Кожа")
        cls.spec_location = SpecLocation.objects.create(
            name="Эпидермис",
            location=cls.location
        )
        cls.complication = Complication.objects.create(
            name="Дерматит",
            alt_name="Радиационный дерматит",
            spec_location=cls.spec_location,
            note="Покраснение и шелушение кожи"
        )

    def test_complication_creation(self):
        self.assertEqual(self.complication.name, "Дерматит")
        self.assertEqual(self.complication.alt_name, "Радиационный дерматит")
        self.assertEqual(self.complication.spec_location.name, "Эпидермис")
        self.assertEqual(self.complication.note, "Покраснение и шелушение кожи")
    
    def test_name_uniqueness(self):
        duplicate = Complication(name="Дерматит")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.complication),
            "Осложнение: Дерматит, Альтернативное название: Радиационный дерматит, Локализация: Эпидермис (Кожа), Доп. информация: Покраснение и шелушение кожи"
        ) 
        
class HistologyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.histology = Histology.objects.create(
            name="Аденокарцинома",
            note="Злокачественная опухоль железистого эпителия"
        )

    def test_histology_creation(self):
        self.assertEqual(self.histology.name, "Аденокарцинома")
        self.assertEqual(self.histology.note, "Злокачественная опухоль железистого эпителия")
    
    def test_name_uniqueness(self):
        duplicate = Histology(name="Аденокарцинома")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.histology),
            "Аденокарцинома Злокачественная опухоль железистого эпителия"
        ) 
        
class ClinicalCaseComplicationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем необходимые зависимости
        cls.diagnosis = Diagnosis.objects.create(
            code="C50", 
            description="Рак молочной железы"
        )
        cls.location = Location.objects.create(name="Грудь")
        cls.spec_location = SpecLocation.objects.create(
            name="Молочная железа",
            location=cls.location
        )
        cls.therapy_type = RadiationTherapyType.objects.create(
            name="Внешнее облучение"
        )
        cls.case = ClinicalCase.objects.create(
            spec_location=cls.spec_location,
            radiation_therapy_type=cls.therapy_type
        )
        cls.complication = Complication.objects.create(
            name="Фиброз"
        )
        cls.case_complication = ClinicalCaseComplication.objects.create(
            clinical_case=cls.case,
            complication=cls.complication
        )

    def test_relationship_creation(self):
        self.assertEqual(self.case_complication.clinical_case, self.case)
        self.assertEqual(self.case_complication.complication, self.complication)
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.case_complication),
            f"{self.case} - Осложнение: {self.complication}"
        )
    
    def test_cascade_delete_clinical_case(self):
        case_id = self.case.id
        self.case.delete()
        self.assertEqual(
            ClinicalCaseComplication.objects.filter(id=self.case_complication.id).count(),
            0
        )
    
    def test_cascade_delete_complication(self):
        complication_id = self.complication.id
        self.complication.delete()
        self.assertEqual(
            ClinicalCaseComplication.objects.filter(id=self.case_complication.id).count(),
            0
        )
        
        
class ModelNameModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = ModelName.objects.create(
            name="LKB",
            full_name="Lyman-Kutcher-Burman",
            model_type=ModelName.ModelTypeChoises.NTCP,
            note="Модель для расчета NTCP"
        )

    def test_model_creation(self):
        self.assertEqual(self.model.name, "LKB")
        self.assertEqual(self.model.full_name, "Lyman-Kutcher-Burman")
        self.assertEqual(self.model.model_type, ModelName.ModelTypeChoises.NTCP)
        self.assertEqual(self.model.note, "Модель для расчета NTCP")
    
    def test_name_uniqueness(self):
        duplicate = ModelName(name="LKB")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        expected = (
            "Модель: LKB(Lyman-Kutcher-Burman), "
            "Тип модели: Normal Tissue Complication Probability (NTCP), "
            "Доп. информация: Модель для расчета NTCP"
        )
        self.assertEqual(str(self.model), expected)                     
        
class RiskGroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.risk_group = RiskGroup.objects.create(
            name="Высокий риск",
            note="Пациенты с множественными факторами риска"
        )

    def test_risk_group_creation(self):
        self.assertEqual(self.risk_group.name, "Высокий риск")
        self.assertEqual(self.risk_group.note, "Пациенты с множественными факторами риска")
    
    def test_optional_fields(self):
        risk = RiskGroup.objects.create()
        self.assertIsNone(risk.name)
        self.assertIsNone(risk.note)
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.risk_group),
            "Риск: Высокий риск, Описание: Пациенты с множественными факторами риска"
        )
    
    def test_verbose_names(self):
        meta = RiskGroup._meta
        self.assertEqual(meta.verbose_name, "Риск")
        self.assertEqual(meta.verbose_name_plural, "Риски")
        
class TumorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tumor = Tumor.objects.create(
            short_name="T2",
            name="Опухоль размером 2-5 см",
            note="Без инвазии окружающих тканей"
        )

    def test_tumor_creation(self):
        self.assertEqual(self.tumor.short_name, "T2")
        self.assertEqual(self.tumor.name, "Опухоль размером 2-5 см")
        self.assertEqual(self.tumor.note, "Без инвазии окружающих тканей")
    
    def test_short_name_uniqueness(self):
        duplicate = Tumor(short_name="T2")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        expected = "T2 (Опухоль размером 2-5 см) Без инвазии окружающих тканей"
        self.assertEqual(str(self.tumor), expected)
    
    def test_verbose_names(self):
        meta = Tumor._meta
        self.assertEqual(meta.verbose_name, "Опухоль")
        self.assertEqual(meta.verbose_name_plural, "Опухоли")
        
class NodeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.node = Node.objects.create(
            short_name="N1",
            name="Метастазы в регионарных лимфоузлах",
            note="На стороне первичной опухоли"
        )

    def test_node_creation(self):
        self.assertEqual(self.node.short_name, "N1")
        self.assertEqual(self.node.name, "Метастазы в регионарных лимфоузлах")
        self.assertEqual(self.node.note, "На стороне первичной опухоли")
    
    def test_short_name_uniqueness(self):
        duplicate = Node(short_name="N1")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        expected = "N1 (Метастазы в регионарных лимфоузлах) На стороне первичной опухоли"
        self.assertEqual(str(self.node), expected)
    
    def test_verbose_names(self):
        meta = Node._meta
        self.assertEqual(meta.verbose_name, "Узлы")
        self.assertEqual(meta.verbose_name_plural, "Узлы")
        
class MetastasisModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.metastasis = Metastasis.objects.create(
            short_name="M1",
            name="Отдаленные метастазы",
            note="Включая поражение других органов"
        )

    def test_metastasis_creation(self):
        self.assertEqual(self.metastasis.short_name, "M1")
        self.assertEqual(self.metastasis.name, "Отдаленные метастазы")
        self.assertEqual(self.metastasis.note, "Включая поражение других органов")
    
    def test_short_name_uniqueness(self):
        duplicate = Metastasis(short_name="M1")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        expected = "M1 (Отдаленные метастазы) Включая поражение других органов"
        self.assertEqual(str(self.metastasis), expected)
    
    def test_verbose_names(self):
        meta = Metastasis._meta
        self.assertEqual(meta.verbose_name, "Метастазы")
        self.assertEqual(meta.verbose_name_plural, "Метастазы")
        
class GradeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.grade = Grade.objects.create(
            name="G2",
            note="Умеренно дифференцированная опухоль"
        )

    def test_grade_creation(self):
        self.assertEqual(self.grade.name, "G2")
        self.assertEqual(self.grade.note, "Умеренно дифференцированная опухоль")
    
    def test_name_uniqueness(self):
        duplicate = Grade(name="G2")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        self.assertEqual(
            str(self.grade),
            "G2 Умеренно дифференцированная опухоль"
        )
    
    def test_verbose_names(self):
        meta = Grade._meta
        self.assertEqual(meta.verbose_name, "Степень злокачественности")
        self.assertEqual(meta.verbose_name_plural, "Степени злокачественности")
        
class UnitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.unit = Unit.objects.create(
            name="Гр",
            full_name="Грей",
            note="Единица поглощенной дозы ионизирующего излучения"
        )

    def test_unit_creation(self):
        self.assertEqual(self.unit.name, "Гр")
        self.assertEqual(self.unit.full_name, "Грей")
        self.assertEqual(self.unit.note, "Единица поглощенной дозы ионизирующего излучения")
    
    def test_name_uniqueness(self):
        duplicate = Unit(name="Гр")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
    
    def test_string_representation(self):
        expected = "Единица измерения: Гр (Грей), Доп. информация: Единица поглощенной дозы ионизирующего излучения"
        self.assertEqual(str(self.unit), expected)
    
    def test_verbose_names(self):
        meta = Unit._meta
        self.assertEqual(meta.verbose_name, "Единица измерения")
        self.assertEqual(meta.verbose_name_plural, "Единицы измерения")
        
class ParameterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.unit = Unit.objects.create(name="Гр")
        cls.parameter = Parameter.objects.create(
            name="D50",
            full_name="Доза, дающая 50% эффекта",
            unit=cls.unit,
            note="Параметр модели LQ"
        )

    def test_parameter_creation(self):
        self.assertEqual(self.parameter.name, "D50")
        self.assertEqual(self.parameter.full_name, "Доза, дающая 50% эффекта")
        self.assertEqual(self.parameter.unit.name, "Гр")
        self.assertEqual(self.parameter.note, "Параметр модели LQ")
    
    def test_string_representation(self):
        expected = "Параметр: D50, Полное название: Доза, дающая 50% эффекта, Ед. изм.: Гр, Доп. информация: Параметр модели LQ"
        self.assertEqual(str(self.parameter), expected)
    
    def test_verbose_names(self):
        meta = Parameter._meta
        self.assertEqual(meta.verbose_name, "Параметр")
        self.assertEqual(meta.verbose_name_plural, "Параметры")
        
        
class ModelStructureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = ModelName.objects.create(
            name="LQ",
            model_type=ModelName.ModelTypeChoises.TCP
        )
        cls.unit = Unit.objects.create(name="Гр")
        cls.parameter = Parameter.objects.create(
            name="α/β",
            unit=cls.unit
        )
        cls.structure = ModelStructure.objects.create(
            model_name=cls.model,
            parameter=cls.parameter,
            note="Отношение альфа/бета"
        )

    def test_structure_creation(self):
        self.assertEqual(self.structure.model_name.name, "LQ")
        self.assertEqual(self.structure.parameter.name, "α/β")
        self.assertEqual(self.structure.note, "Отношение альфа/бета")
    
    def test_string_representation(self):
        # Ожидаем строку с учетом полного представления ModelName
        expected = (
            "Структура модели: Модель: LQ, Тип модели: Tumor Control Probability (TCP), "
            "Параметр: Параметр: α/β, Ед. изм.: Гр, "
            "Доп. информация: Отношение альфа/бета"
        )
        self.assertEqual(str(self.structure), expected)
    
    def test_verbose_names(self):
        meta = ModelStructure._meta
        self.assertEqual(meta.verbose_name, "Структура модели")
        self.assertEqual(meta.verbose_name_plural, "Структуры моделей")
        
class SourceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.source = Source.objects.create(
            name="PMID:12345678",
            full_name="Journal of Radiation Oncology, 2023",
            url="https://example.com/article",
            note="Основной источник данных"
        )

    def test_source_creation(self):
        self.assertEqual(self.source.name, "PMID:12345678")
        self.assertEqual(self.source.full_name, "Journal of Radiation Oncology, 2023")
        self.assertEqual(self.source.url, "https://example.com/article")
        self.assertEqual(self.source.note, "Основной источник данных")
    
    def test_string_representation(self):
        expected = "Источник: PMID:12345678, Полное название: Journal of Radiation Oncology, 2023, Ссылка: https://example.com/article, Доп. информация: Основной источник данных"
        self.assertEqual(str(self.source), expected)
    
    def test_verbose_names(self):
        meta = Source._meta
        self.assertEqual(meta.verbose_name, "Источник")
        self.assertEqual(meta.verbose_name_plural, "Источники")
        

class DataSetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем зависимости
        cls.diagnosis = Diagnosis.objects.create(code="C50", description="Рак молочной железы")
        cls.location = Location.objects.create(name="Грудь")
        cls.spec_location = SpecLocation.objects.create(name="Молочная железа", location=cls.location)
        cls.therapy_type = RadiationTherapyType.objects.create(name="Внешнее облучение")
        cls.case = ClinicalCase.objects.create(
            spec_location=cls.spec_location,
            radiation_therapy_type=cls.therapy_type
        )
        cls.source = Source.objects.create(name="Источник 1")
        
        cls.dataset = DataSet.objects.create(
            clinical_case=cls.case,
            source=cls.source,
            note="Набор данных для анализа"
        )

    def test_dataset_creation(self):
        self.assertEqual(self.dataset.clinical_case.spec_location.name, "Молочная железа")
        self.assertEqual(self.dataset.source.name, "Источник 1")
        self.assertEqual(self.dataset.note, "Набор данных для анализа")
    
    def test_string_representation(self):
        expected = "Клинический случай: Количество: 1, Пол: Неизвестно, Локализация: Молочная железа (Грудь), Вид терапии: Внешнее облучение, Источник: Источник: Источник 1, Доп. информация: Набор данных для анализа"
        self.assertIn("Клинический случай:", str(self.dataset))
        self.assertIn("Источник: Источник 1", str(self.dataset))
    
    def test_verbose_names(self):
        meta = DataSet._meta
        self.assertEqual(meta.verbose_name, "Набор данных")
        self.assertEqual(meta.verbose_name_plural, "Наборы данных")
        
class ResultModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем сложные зависимости
        cls.model = ModelName.objects.create(name="LQ")
        cls.unit = Unit.objects.create(name="Гр")
        cls.parameter = Parameter.objects.create(name="α", unit=cls.unit)
        cls.structure = ModelStructure.objects.create(
            model_name=cls.model,
            parameter=cls.parameter
        )
        
        cls.dataset = DataSet.objects.create()
        
        cls.result = Result.objects.create(
            model_structure=cls.structure,
            value=0.35,
            upper_value=0.40,
            lower_value=0.30,
            note="Результат расчета",
            data_set=cls.dataset
        )

    def test_result_creation(self):
        self.assertEqual(self.result.value, 0.35)
        self.assertEqual(self.result.upper_value, 0.40)
        self.assertEqual(self.result.lower_value, 0.30)
        self.assertEqual(self.result.note, "Результат расчета")
        self.assertEqual(self.result.model_structure.parameter.name, "α")
        self.assertEqual(self.result.data_set, self.dataset)
    
    def test_string_representation(self):
        expected = "Структура модели: Модель: LQ, Параметр: Параметр: α, Ед. изм.: Гр Результат: 0.35, Верхняя граница: 0.4, Нижняя граница: 0.3, Доп. информация: Результат расчета"
        self.assertIn("Результат: 0.35", str(self.result))
        self.assertIn("Верхняя граница: 0.4", str(self.result))
        self.assertIn("Нижняя граница: 0.3", str(self.result))
    
    def test_verbose_names(self):
        meta = Result._meta
        self.assertEqual(meta.verbose_name, "Результат измерения")
        self.assertEqual(meta.verbose_name_plural, "Результаты измерений")
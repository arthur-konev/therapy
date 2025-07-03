import time
import unittest
from django.test import TestCase
from django.urls import reverse
from django.db import connection, reset_queries
from rest_framework.test import APIClient
from users.models import GeneralUser as User
from therapy.models import (
    ClinicalCase, SpecLocation, Location, Diagnosis, Complication,
    DataSet, Result, ModelStructure, ModelName, Parameter, Unit,
    RadiationTherapyType, Stage, RiskGroup, Histology, Grade, Tumor, Node, Metastasis,ClinicalCaseComplication 
)
from django.conf import settings
from django.db import connection

settings.DEBUG = True
connection.force_debug_cursor = True

class PerformanceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных для всех тестов производительности"""
        cls.user = User.objects.create_user(username='perfuser', password='testpass')
        
        # Создаем базовые объекты
        loc = Location.objects.create(name='Test Location')
        cls.spec_loc = SpecLocation.objects.create(location=loc, name='Test Spec Location')
        cls.diagnosis = Diagnosis.objects.create(code='C00', description='Test Diagnosis')
        cls.complication = Complication.objects.create(name='Test Complication', spec_location=cls.spec_loc)
        cls.stage = Stage.objects.create(name='Stage I')
        cls.risk_group = RiskGroup.objects.create(name='Low Risk')
        cls.rt_type = RadiationTherapyType.objects.create(name='EBRT')
        cls.histology = Histology.objects.create(name='Adenocarcinoma')
        cls.grade = Grade.objects.create(name='G2')
        cls.tumor = Tumor.objects.create(short_name='T1', name='Tumor Stage 1')
        cls.node = Node.objects.create(short_name='N0', name='No Nodes')
        cls.metastasis = Metastasis.objects.create(short_name='M0', name='No Metastasis')
        
        # Создаем модель и параметры
        cls.unit = Unit.objects.create(name='Gy')
        cls.parameter = Parameter.objects.create(name='Dose', unit=cls.unit)
        cls.model_name = ModelName.objects.create(name='NTCP Model')
        cls.model_struct = ModelStructure.objects.create(
            model_name=cls.model_name, 
            parameter=cls.parameter
        )
        
        # Создаем 1000 клинических случаев
        cases = []
        for i in range(1000):
            case = ClinicalCase(
                spec_location=cls.spec_loc,
                diagnosis=cls.diagnosis,
                gender=1 if i % 2 == 0 else 2,
                age=30 + i % 50,
                number_of_fractions=25 + i % 10,
                single_dose=1.8 + i % 10 * 0.1,
                treatment_duration=30 + i % 20,
                stage=cls.stage,
                risk_group=cls.risk_group,
                radiation_therapy_type=cls.rt_type,
                histology=cls.histology,
                grade=cls.grade,
                tumor=cls.tumor,
                node=cls.node,
                metastasis=cls.metastasis
            )
            cases.append(case)
        
        ClinicalCase.objects.bulk_create(cases, batch_size=500)
        
        # Создаем наборы данных и результаты
        datasets = []
        results = []
        
        # Для каждого случая создаем по 3 результата
        for case in ClinicalCase.objects.all():
            dataset = DataSet(
                clinical_case=case,
                source=None
            )
            datasets.append(dataset)
        
        DataSet.objects.bulk_create(datasets, batch_size=500)
        
        # Создаем результаты измерений
        for dataset in DataSet.objects.all():
            for _ in range(3):
                result = Result(
                    data_set=dataset,
                    model_structure=cls.model_struct,
                    value=10.0 + dataset.id % 10
                )
                results.append(result)
        
        Result.objects.bulk_create(results, batch_size=1000)
        
        # Создаем связи осложнений
        complications = []
        for case in ClinicalCase.objects.all():
            complication = ClinicalCaseComplication(
                clinical_case=case,
                complication=cls.complication
            )
            complications.append(complication)
        
        ClinicalCaseComplication.objects.bulk_create(complications, batch_size=500)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_complex_filter_performance(self):
        """Тест производительности сложной фильтрации клинических случаев"""
        url = reverse('clinical-case-list')
        
        # Сбросим счетчик запросов
        reset_queries()
        
        start_time = time.perf_counter()
        
        response = self.client.get(url, {
            'location': self.spec_loc.location.id,
            'age_min': 30,
            'age_max': 60,
            'gender': 1,
            'number_of_fractions': 30,
            'complication': self.complication.id,
            'stage': self.stage.id,
            'risk_group': self.risk_group.id,
            'radiation_therapy_type': self.rt_type.id,
            'histology': self.histology.id,
            'grade': self.grade.id
        })
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        print(f"\n[Фильтрация] Время: {execution_time:.4f}с, "
              f"Запросов: {len(connection.queries)}, "
              f"Результатов: {len(response.data)}")
        
        # Проверяем, что не делаем N+1 запросов
        self.assertLess(len(connection.queries), 15)
        self.assertLess(execution_time, 1.0)

    def test_aggregation_performance(self):
        """Тест производительности агрегации данных"""
        url = reverse('aggregate-metrics-list')
        
        # Получаем ID всех клинических случаев
        case_ids = list(ClinicalCase.objects.values_list('id', flat=True)[:500])
        
        reset_queries()
        start_time = time.perf_counter()
        
        response = self.client.post(url, {
            "clinical_case_ids": case_ids
        }, format='json')
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        print(f"\n[Агрегация] Время: {execution_time:.4f}с, "
              f"Запросов: {len(connection.queries)}, "
              f"Параметров: {len(response.data['aggregated_parameters'])}")
        
        # Проверяем эффективность запросов
        self.assertLess(len(connection.queries), 10)
        self.assertLess(execution_time, 1.5)

    def test_bulk_create_performance(self):
        """Тест производительности массового создания объектов"""
        url = reverse('clinical-case-list')
        
        # Подготовка данных для 100 новых случаев
        data_list = [
            {
                "spec_location": self.spec_loc.id,
                "diagnosis": self.diagnosis.id,
                "gender": 1 if i % 2 == 0 else 2,
                "age": 40 + i,
                "number_of_fractions": 28,
                "stage": self.stage.id,
                "risk_group": self.risk_group.id,
                "radiation_therapy_type": self.rt_type.id,
                "histology": self.histology.id,
                "grade": self.grade.id,
                "quantity": 1
            } for i in range(100)
        ]
        
        reset_queries()
        start = time.perf_counter()
        
        created_count = 0
        for payload in data_list:
            resp = self.client.post(url, payload, format='json')
            self.assertEqual(resp.status_code, 201)
            created_count += 1

        elapsed = time.perf_counter() - start
        print(f"\n[Создание] Время на 100 POST: {elapsed:.4f}s, Запросов: {len(connection.queries)}")
        self.assertEqual(created_count, 100)
        self.assertLess(len(connection.queries), 120)
        self.assertLess(elapsed, 5.0)  


    def test_query_scalability(self):
        """Тест масштабируемости при увеличении объема данных"""
        url = reverse('clinical-case-list')
        
        # Измеряем время для разного количества объектов
        for count in [100, 500, 1000, 2000]:
            # Создаем временные данные
            ClinicalCase.objects.all().delete()
            cases = [ClinicalCase(
                spec_location=self.spec_loc,
                diagnosis=self.diagnosis,
                gender=1,
                age=50,
                radiation_therapy_type= self.rt_type,
            ) for _ in range(count)]
            ClinicalCase.objects.bulk_create(cases, batch_size=500)
            
            reset_queries()
            start_time = time.perf_counter()
            
            self.client.get(url, {'location': self.spec_loc.location.id})
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            query_count = len(connection.queries)
            
            print(f"\n[Масштабируемость] {count} записей: "
                  f"{execution_time:.4f}с, {query_count} запросов")
            
            # Проверяем что время растет линейно или лучше
            if count > 100:
                time_per_record = execution_time / count
                self.assertLess(time_per_record, 0.01)

    def test_index_usage_performance(self):
        """Тест эффективности использования индексов"""
        url = reverse('clinical-case-list')
        
        # Тест без фильтра по индексированному полю
        reset_queries()
        start_time = time.perf_counter()
        response = self.client.get(url)
        end_time = time.perf_counter()
        time_without_index = end_time - start_time
        
        # Тест с фильтром по индексированному полю
        reset_queries()
        start_time = time.perf_counter()
        response = self.client.get(url, {'age': 40})
        end_time = time.perf_counter()
        time_with_index = end_time - start_time
        
        print(f"\n[Индексы] Без индекса: {time_without_index:.4f}с, "
              f"С индексом: {time_with_index:.4f}с")
        
        # Проверяем что фильтрация по индексированному полю быстрее
        self.assertLess(time_with_index, time_without_index)

    def test_heavy_aggregation_performance(self):
        """Тест производительности сложной агрегации с группировкой"""
        # Создаем дополнительные данные для агрегации
        unit2 = Unit.objects.create(name='%')
        parameter2 = Parameter.objects.create(name='Probability', unit=unit2)
        model_struct2 = ModelStructure.objects.create(
            model_name=self.model_name, 
            parameter=parameter2
        )
        
        # Добавляем дополнительные результаты
        new_results = []
        for dataset in DataSet.objects.all()[:500]:
            result = Result(
                data_set=dataset,
                model_structure=model_struct2,
                value=50 + dataset.id % 50
            )
            new_results.append(result)
        
        Result.objects.bulk_create(new_results, batch_size=500)
        
        url = reverse('aggregate-metrics-list')
        case_ids = list(ClinicalCase.objects.values_list('id', flat=True))
        
        reset_queries()
        start_time = time.perf_counter()
        
        response = self.client.post(url, {
            "clinical_case_ids": case_ids
        }, format='json')
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        print(f"\n[Сложная агрегация] Время: {execution_time:.4f}с, "
              f"Параметров: {len(response.data['aggregated_parameters'])}")
        
        # Проверяем что все данные корректно агрегированы
        self.assertEqual(len(response.data['aggregated_parameters']), 2)
        self.assertLess(execution_time, 3.0)

    def test_complex_join_performance(self):
        """Тест производительности сложных JOIN-запросов"""
        url = reverse('result-list')
        
        # Фильтр с глубокими связями
        params = {
            'clinical_case': ClinicalCase.objects.first().id,
            'model_structure__model_name__name': 'NTCP Model',
            'model_structure__parameter__name': 'Dose'
        }
        
        settings.DEBUG = True
        connection.force_debug_cursor = True
        reset_queries()
        
        start_time = time.perf_counter()
        response = self.client.get(url, params)
        end_time = time.perf_counter()
        
        # теперь connection.queries действительно содержит SQL
        query_count = len(connection.queries)

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        # проверяем, что Django отправил ровно один SQL
        self.assertEqual(query_count, 1)
        self.assertLess(end_time - start_time, 0.5)

        # возвращаем DEBUG в исходное состояние (если нужно)
        settings.DEBUG = False
        connection.force_debug_cursor = False

    def test_memory_usage(self):
        """Тест использования памяти при обработке больших наборов данных"""
        import tracemalloc
        url = reverse('clinical-case-list')
        
        # Запускаем отслеживание памяти
        tracemalloc.start()
        
        snapshot1 = tracemalloc.take_snapshot()
        response = self.client.get(url)
        snapshot2 = tracemalloc.take_snapshot()
        
        # Вычисляем разницу в памяти
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        total_memory = sum(stat.size for stat in top_stats)
        
        print(f"\n[Память] Использовано: {total_memory / 1024:.2f} KB")
        
        # Проверяем что использование памяти в разумных пределах
        self.assertLess(total_memory, 58 * 1024 * 1024)  # < 58 MB
        
        tracemalloc.stop()

if __name__ == '__main__':
    unittest.main()
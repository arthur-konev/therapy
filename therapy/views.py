from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
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
    RadiationTherapyType,
    Histology,
    Grade,
    Tumor,
    Node,
    Metastasis,
    ClinicalCaseComplication,
)
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from .serializers import (
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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets, permissions, filters

from django.db.models import Count
from collections import defaultdict
from rest_framework.views import APIView

# from .permissions import NotBobPermission


class RadiationTherapyTypeViewSet(viewsets.ModelViewSet):
    serializer_class = RadiationTherapyTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name", "note"]
    ordering_fields = ["name", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return RadiationTherapyType.objects.all()


class ClinicalCaseComplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalCaseComplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["clinical_case"]
    search_fields = ["clinical_case", "complication"]
    ordering_fields = ["clinical_case", "complication"]
    ordering = ["clinical_case"]

    def get_queryset(self):
        return ClinicalCaseComplication.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name", "short_name", "note"]
    search_fields = ["name", "short_name", "note"]
    ordering_fields = ["name", "short_name", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return Location.objects.all()


class SpecLocationViewSet(viewsets.ModelViewSet):
    serializer_class = SpecLocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["location", "name"]
    search_fields = ["name", "note", "location__name"]
    ordering_fields = ["name", "location", "note"]
    ordering = ["name"]

    def get_queryset(self):

        return SpecLocation.objects.all()


class SpecLocationViewSet(viewsets.ModelViewSet):
    serializer_class = SpecLocationSerializer
    permission_classes = (permissions.IsAuthenticated,) 

    filter_backends = [
        DjangoFilterBackend,    
        filters.SearchFilter,   
        filters.OrderingFilter, 
    ]
    
    # Поля, по которым можно фильтровать результаты через параметры запроса.
    filterset_fields = ["location", "name"]
    # Например, поиск по имени, заметкам, а также по имени связанной локализации.
    search_fields = ["name", "note", "location__name"]
    # Поля, по которым можно сортировать результаты.
    ordering_fields = ["name", "location", "note"]
    
    # Поле сортировки по умолчанию, если пользователь не указал иное.
    ordering = ["name"]

    def get_queryset(self):
        return SpecLocation.objects.all()



class DiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["code", "description", "note"]
    search_fields = ["code", "description", "note"]
    ordering_fields = ["code", "description", "note"]
    ordering = ["code"]

    def get_queryset(self):

        return Diagnosis.objects.all()


class StageViewSet(viewsets.ModelViewSet):
    serializer_class = StageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name", "note"]
    ordering_fields = ["name", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return Stage.objects.all()


class RiskGroupViewSet(viewsets.ModelViewSet):
    serializer_class = RiskGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name", "note"]
    ordering_fields = ["name", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return RiskGroup.objects.all()


class ComplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ComplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name", "alt_name", "spec_location", "note"]
    search_fields = ["name", "alt_name", "spec_location__name", "note"]
    ordering_fields = ["name", "alt_name", "spec_location", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return Complication.objects.all()


class HistologyViewSet(viewsets.ModelViewSet):
    serializer_class = HistologySerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name", "note"]
    ordering_fields = ["name", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return Histology.objects.all()


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name", "note"]
    ordering_fields = ["name", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return Grade.objects.all()


class TumorViewSet(viewsets.ModelViewSet):
    serializer_class = TumorSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["short_name", "name"]
    search_fields = ["short_name", "name", "note"]
    ordering_fields = ["short_name", "name", "note"]
    ordering = ["short_name"]

    def get_queryset(self):
        return Tumor.objects.all()


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["short_name", "name"]
    search_fields = ["short_name", "name", "note"]
    ordering_fields = ["short_name", "name", "note"]
    ordering = ["short_name"]

    def get_queryset(self):
        return Node.objects.all()


class MetastasisViewSet(viewsets.ModelViewSet):
    serializer_class = MetastasisSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["short_name", "name"]
    search_fields = ["short_name", "name", "note"]
    ordering_fields = ["short_name", "name", "note"]
    ordering = ["short_name"]

    def get_queryset(self):
        return Metastasis.objects.all()


class ClinicalCaseViewSet(viewsets.ModelViewSet):

    serializer_class = ClinicalCaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = ClinicalCase.objects.all()
        location_filter = self.request.query_params.get("location")
        age_filter = self.request.query_params.get("age")
        age_min_filter = self.request.query_params.get("age_min")
        age_max_filter = self.request.query_params.get("age_max")
        quantity_filter = self.request.query_params.get("quantity")
        gender_filter = self.request.query_params.get("gender")
        diagnosis_filter = self.request.query_params.get("diagnosis")
        spec_location_filter = self.request.query_params.get("spec_location")
        complication_filter = self.request.query_params.get("complication")
        stage_filter = self.request.query_params.get("stage")
        risk_group_filter = self.request.query_params.get("risk_group")
        radiation_therapy_type_filter = self.request.query_params.get(
            "radiation_therapy_type"
        )
        tumor_filter = self.request.query_params.get("tumor")
        node_filter = self.request.query_params.get("node")
        metastasis_filter = self.request.query_params.get("metastasis")
        histology_filter = self.request.query_params.get("histology")
        grade_filter = self.request.query_params.get("grade")
        number_of_fractions_filter = self.request.query_params.get(
            "number_of_fractions"
        )
        single_dose_filter = self.request.query_params.get("single_dose")
        treatment_duration_filter = self.request.query_params.get("treatment_duration")
        
        result_filter = self.request.query_params.get("result")
        dataset_filter = self.request.query_params.get("dataset")
        source_filter = self.request.query_params.get("source")
        model_structure_filter = self.request.query_params.get("model_structure")
        model_name_filter = self.request.query_params.get("model_name")
        parameter_filter = self.request.query_params.get("parameter")

        location_list = []
        age_list = []
        age_min_list = []
        gender_list = []
        quantity_list = []
        diagnosis_list = []
        spec_location_list = []
        complication_list = []
        stage_list = []
        risk_group_list = []
        radiation_therapy_type_list = []
        tumor_list = []
        node_list = []
        metastasis_list = []
        histology_list = []
        grade_list = []
        number_of_fractions_list = []
        single_dose_list = []
        treatment_duration_list = []

        if result_filter:
            result_list = result_filter.split(",")
            queryset = queryset.filter(dataset__result__in=result_list)

        if dataset_filter:
            dataset_list = dataset_filter.split(",")
            queryset = queryset.filter(dataset__in=dataset_list)

        if source_filter:
            source_list = source_filter.split(",")
            queryset = queryset.filter(dataset__source__in=source_list)

        if model_structure_filter:
            ms_list = model_structure_filter.split(",")
            queryset = queryset.filter(dataset__result__model_structure__in=ms_list)

        if model_name_filter:
            mn_list = model_name_filter.split(",")
            queryset = queryset.filter(dataset__result__model_structure__model_name__in=mn_list)

        if parameter_filter:
            param_list = parameter_filter.split(",")
            queryset = queryset.filter(dataset__result__model_structure__parameter__in=param_list)
            
        if age_filter:
            age_list = age_filter.split(",")
            queryset = queryset.filter(age__in=age_list)
        if location_filter:
            location_list = location_filter.split(",")
            queryset = queryset.filter(spec_location__location__in=location_list)
        if age_min_filter:
            age_min_list = age_min_filter.split(",")
            queryset = queryset.filter(age_min__in=age_min_list)
        if gender_filter:
            gender_list = gender_filter.split(",")
            queryset = queryset.filter(gender__in=gender_list)
        if age_max_filter:
            age_max_list = age_max_filter.split(",")
            queryset = queryset.filter(age_max__in=age_max_list)
        if quantity_filter:
            quantity_list = quantity_filter.split(",")
            queryset = queryset.filter(quantity__in=quantity_list)
        if diagnosis_filter:
            diagnosis_list = diagnosis_filter.split(",")
            queryset = queryset.filter(diagnosis__in=diagnosis_list)
        if spec_location_filter:
            spec_location_list = spec_location_filter.split(",")
            queryset = queryset.filter(spec_location__in=spec_location_list)
        if complication_filter:
            complication_list = complication_filter.split(",")
            queryset = queryset.filter(clinicalcasecomplication__complication__in=complication_list)
        if stage_filter:
            stage_list = stage_filter.split(",")
            queryset = queryset.filter(stage__in=stage_list)
        if risk_group_filter:
            risk_group_list = risk_group_filter.split(",")
            queryset = queryset.filter(risk_group__in=risk_group_list)
        if radiation_therapy_type_filter:
            radiation_therapy_type_list = radiation_therapy_type_filter.split(",")
            queryset = queryset.filter(
                radiation_therapy_type__in=radiation_therapy_type_list
            )
        if tumor_filter:
            tumor_list = tumor_filter.split(",")
            queryset = queryset.filter(tumor__in=tumor_list)
        if node_filter:
            node_list = node_filter.split(",")
            queryset = queryset.filter(node__in=node_list)
        if metastasis_filter:
            metastasis_list = metastasis_filter.split(",")
            queryset = queryset.filter(metastasis__in=metastasis_list)
        if histology_filter:
            histology_list = histology_filter.split(",")
            queryset = queryset.filter(histology__in=histology_list)
        if grade_filter:
            grade_list = grade_filter.split(",")
            queryset = queryset.filter(grade__in=grade_list)
        if number_of_fractions_filter:
            number_of_fractions_list = number_of_fractions_filter.split(",")
            queryset = queryset.filter(number_of_fractions__in=number_of_fractions_list)
        if single_dose_filter:
            single_dose_list = single_dose_filter.split(",")
            queryset = queryset.filter(single_dose__in=single_dose_list)
        if treatment_duration_filter:
            treatment_duration_list = treatment_duration_filter.split(",")
            queryset = queryset.filter(treatment_duration__in=treatment_duration_list)

        return queryset

    def create(self, request, *args, **kwargs):
        # если пришёл список – делаем bulk_create
        if isinstance(request.data, list):
            serializers = [ self.get_serializer(data=item) for item in request.data ]
            # проверяем валидность каждого
            for ser in serializers:
                ser.is_valid(raise_exception=True)
            # собираем списком объекты (но не сохраняем через .save())
            objs = [ ClinicalCase(**ser.validated_data) for ser in serializers ]
            ClinicalCase.objects.bulk_create(objs)
            # формируем ответ – можно вернуть просто список «id» новых объектов
            created_ids = [ obj.id for obj in objs ]
            return Response({'created_ids': created_ids}, status=status.HTTP_201_CREATED)
        # иначе – как обычно
        return super().create(request, *args, **kwargs)

class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["full_name", "name"]
    search_fields = ["full_name", "name", "note"]
    ordering_fields = ["full_name", "name", "note"]
    ordering = ["name"]

    def get_queryset(self):
        return Unit.objects.all()


class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["full_name", "name", "unit"]
    search_fields = ["full_name", "name", "note", "unit__name", "unit__full_name"]
    ordering_fields = ["full_name", "name", "note", "unit"]
    ordering = ["name"]

    def get_queryset(self):
        return Parameter.objects.all()


class ModelNameViewSet(viewsets.ModelViewSet):
    serializer_class = ModelNameSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["full_name", "name", "model_type"]
    search_fields = ["full_name", "name", "note", "model_type"]
    ordering_fields = ["full_name", "name", "note", "model_type"]
    ordering = ["name"]

    def get_queryset(self):
        return ModelName.objects.all()


class ModelStructureViewSet(viewsets.ModelViewSet):
    serializer_class = ModelStructureSerializer
    permission_classes = (permissions.IsAuthenticated,) 
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "model_name",
        "parameter",
    ]
    search_fields = [
        "model_name__name",
        "model_name__full_name",
        "model_name__model_type",
        "parameter__full_name",
        "parameter__name",
        "parameter__unit__name",
        "parameter__unit__full_name",
        "note",
    ]
    ordering_fields = [
        "model_name",
        "parameter",
        "note",
    ]
    ordering = ["model_name"]

    def get_queryset(self):
        return ModelStructure.objects.all()


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["model_structure","value", "upper_value","lower_value","note",
    ]
    search_fields = [
        "model_structure__model_name__name","model_structure__model_name__full_name",
        "model_structure__model_name__model_type",
        "model_structure__parameter__full_name","model_structure__parameter__name",
        "model_structure__parameter__unit__name","model_structure__parameter__unit__full_name",
        "value","upper_value","lower_value","note",
    ]
    ordering_fields = [
        "model_structure","value","upper_value","lower_value","note",
    ]
    ordering = ["model_structure"]

    def get_queryset(self):
        queryset = Result.objects.all()
        clinical_case_id = self.request.query_params.get("clinical_case")

        if clinical_case_id:
            queryset = queryset.filter(data_set__clinical_case__id=clinical_case_id)

        return queryset


class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["full_name", "name", "url"]
    search_fields = ["full_name", "name", "note", "url"]
    ordering_fields = ["full_name", "name", "note", "url"]
    ordering = ["name"]

    def get_queryset(self):
        return Source.objects.all()


class DataSetViewSet(viewsets.ModelViewSet):
    serializer_class = DataSetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {
        "clinical_case",
        "source__name",
        "note",
    }

    search_fields = ["source__name", "note"]
    ordering_fields = ["clinical_case", "source", "note"]
    ordering = ["result"]

    def get_queryset(self):
        return DataSet.objects.all()

class AggregatedMetricsView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request):
        clinical_case_ids = request.data.get("clinical_case_ids", [])

        # Получаем результаты с привязкой к клиническим случаям
        results = Result.objects.filter(
            data_set__clinical_case__id__in=clinical_case_ids,
            value__isnull=False
        ).select_related(
            'model_structure__model_name',
            'model_structure__parameter',
            'model_structure__parameter__unit',
            'data_set__clinical_case'
        )

        # Считаем уникальные случаи и общее количество результатов
        unique_case_count = ClinicalCase.objects.filter(id__in=clinical_case_ids).distinct().count()
        total_result_count = results.count()

        # Группируем значения
        grouped_data = defaultdict(list)

        for r in results:
            model = r.model_structure.model_name.name if r.model_structure and r.model_structure.model_name else None
            param = r.model_structure.parameter.name if r.model_structure and r.model_structure.parameter else "N/A"
            unit = r.model_structure.parameter.unit.name if (
                r.model_structure and 
                r.model_structure.parameter and 
                r.model_structure.parameter.unit
            ) else ""

            case = r.data_set.clinical_case
            meta = {
                "value": r.value,
                "number_of_fractions": case.number_of_fractions,
                "single_dose": case.single_dose,
                "treatment_duration": case.treatment_duration,
                "clinical_case_id": case.id 
            }

            grouped_data[(model, param, unit)].append(meta)

        # Формируем ответ
        aggregated = []
        for (model, param, unit), entries in grouped_data.items():
            values = [e["value"] for e in entries]
            avg = sum(values) / len(values)

            min_entry = min(entries, key=lambda x: x["value"])
            max_entry = max(entries, key=lambda x: x["value"])

            aggregated.append({
                "model": model,
                "parameter": param,
                "unit": unit,
                "count": len(values),
                "average": round(avg, 2),
                "min_value": round(min_entry["value"], 2),
                "min_meta": {
                    "number_of_fractions": min_entry["number_of_fractions"],
                    "single_dose": min_entry["single_dose"],
                    "treatment_duration": min_entry["treatment_duration"],
                    "clinical_case_id": min_entry["clinical_case_id"]
                },
                "max_value": round(max_entry["value"], 2),
                "max_meta": {
                    "number_of_fractions": max_entry["number_of_fractions"],
                    "single_dose": max_entry["single_dose"],
                    "treatment_duration": max_entry["treatment_duration"],
                    "clinical_case_id": max_entry["clinical_case_id"]
                }
            })

        return Response({
            "clinical_case_count": unique_case_count,
            "result_count": total_result_count,
            "aggregated_parameters": aggregated
        })
        
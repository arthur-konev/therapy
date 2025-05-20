from django.shortcuts import render
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
            queryset = queryset.filter(complication__in=complication_list)
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "model_structure",
        "value",
        "upper_value",
        "lower_value",
        "note",
    ]
    search_fields = [
        "model_structure__model_name__name",
        "model_structure__model_name__full_name",
        "model_structure__model_name__model_type",
        "model_structure__parameter__full_name",
        "model_structure__parameter__name",
        "model_structure__parameter__unit__name",
        "model_structure__parameter__unit__full_name",
        "value",
        "upper_value",
        "lower_value",
        "note",
    ]
    ordering_fields = [
        "model_structure",
        "value",
        "upper_value",
        "lower_value",
        "note",
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

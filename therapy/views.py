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
)
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets, permissions
#from .permissions import NotBobPermission

class RadiationTherapyTypeViewSet(viewsets.ModelViewSet):
    serializer_class = RadiationTherapyTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return RadiationTherapyType.objects.filter(name__icontains=name_filter)
        else:
            return RadiationTherapyType.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Location.objects.filter(name__icontains=name_filter)
        else:
            return Location.objects.all()


class SpecLocationViewSet(viewsets.ModelViewSet):
    serializer_class = SpecLocationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return SpecLocation.objects.filter(name__icontains=name_filter)
        else:
            return SpecLocation.objects.all()


class StageViewSet(viewsets.ModelViewSet):
    serializer_class = StageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Stage.objects.filter(name__icontains=name_filter)
        else:
            return Stage.objects.all()


class RiskGroupViewSet(viewsets.ModelViewSet):
    serializer_class = RiskGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return RiskGroup.objects.filter(name__icontains=name_filter)
        else:
            return RiskGroup.objects.all()
  
        
class DiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("code")
        if name_filter:
            return Diagnosis.objects.filter(code__icontains=name_filter)
        else:
            return Diagnosis.objects.all()


class HistologyViewSet(viewsets.ModelViewSet):
    serializer_class = HistologySerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Histology.objects.filter(name__icontains=name_filter)
        else:
            return Histology.objects.all()


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Grade.objects.filter(name__icontains=name_filter)
        else:
            return Grade.objects.all()
   
        
class TumorViewSet(viewsets.ModelViewSet):
    serializer_class = TumorSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("short_name")
        if name_filter:
            return Tumor.objects.filter(short_name__icontains=name_filter)
        else:
            return Tumor.objects.all()


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("short_name")
        if name_filter:
            return Node.objects.filter(short_name__icontains=name_filter)
        else:
            return Node.objects.all()


class MetastasisViewSet(viewsets.ModelViewSet):
    serializer_class = MetastasisSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("short_name")
        if name_filter:
            return Metastasis.objects.filter(short_name__icontains=name_filter)
        else:
            return Metastasis.objects.all()


class ClinicalCaseViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalCaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get_queryset(self):
        age_filter = self.request.query_params.get("age")
        if age_filter:
            # Разделяем значения по запятой и создаем список
            age_list = age_filter.split(',')
            return ClinicalCase.objects.filter(age__in=age_list)
        else:
            return ClinicalCase.objects.all()

class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Unit.objects.filter(name__icontains=name_filter)
        else:
            return Unit.objects.all()

class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Parameter.objects.filter(name__icontains=name_filter)
        else:
            return Parameter.objects.all()

class ModelNameViewSet(viewsets.ModelViewSet):
    serializer_class = ModelNameSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return ModelName.objects.filter(name__icontains=name_filter)
        else:
            return ModelName.objects.all()


class ComplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ComplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Complication.objects.filter(name__icontains=name_filter)
        else:
            return Complication.objects.all()


class ModelStructureViewSet(viewsets.ModelViewSet):
    serializer_class = ModelStructureSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("model_name")
        if name_filter:
            return ModelStructure.objects.filter(model_name__icontains=name_filter)
        else:
            return ModelStructure.objects.all()


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("model_structure")
        if name_filter:
            return Result.objects.filter(model_structure__icontains=name_filter)
        else:
            return Result.objects.all()

class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("name")
        if name_filter:
            return Source.objects.filter(name__icontains=name_filter)
        else:
            return Source.objects.all()


class DataSetViewSet(viewsets.ModelViewSet):
    serializer_class = DataSetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        name_filter = self.request.query_params.get("result")
        if name_filter:
            return DataSet.objects.filter(result__icontains=name_filter)
        else:
            return DataSet.objects.all()





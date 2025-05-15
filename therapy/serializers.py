from rest_framework import serializers
from .models import (
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
)

class RadiationTherapyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiationTherapyType
        fields = ("id", "name", "note")
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name", "short_name", "created_at", "updated_at", "note")


class SpecLocationSerializer(serializers.ModelSerializer):
    name_location = serializers.SerializerMethodField()

    class Meta:
        model = SpecLocation
        fields = ("id", "name", "location", "note","name_location")
    
    def get_name_location(self, obj):
        location = obj.location
        result = f"{obj.location.name}"
        return result


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ("id", "code", "description", "note")

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ("id", "name", "note")


class RiskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskGroup
        fields = ("id", "name", "note")


class ComplicationSerializer(serializers.ModelSerializer):
    
    name_location = serializers.SerializerMethodField()

    class Meta:
        model = Complication
        fields = ("id", "name", "alt_name", "spec_location", "name_location", "note")

    def get_name_location(self, obj):
        location = obj.spec_location
        result = f"{obj.spec_location.name}"
        return result


class HistologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Histology
        fields = ("id", "name", "note")


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ("id", "name", "note")


class TumorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tumor
        fields = ("id", "short_name", "name", "note")


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("id", "short_name", "name", "note")


class MetastasisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metastasis
        fields = ("id", "short_name", "name", "note")
        


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ("id", "name", "full_name", "note")


class ParameterSerializer(serializers.ModelSerializer):
    name_unit = serializers.SerializerMethodField()

    class Meta:
        model = Parameter
        fields = ("id", "name", "full_name", "unit", "note","name_unit")

    def get_name_unit(self, obj):
        unit = obj.unit
        if unit is not None: 
            result = f"{obj.unit.name}"
        else:
            result = "Не указано" 
        return result


class ModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelName
        fields = ("id", "name", "full_name", "model_type", "note")



class ModelStructureSerializer(serializers.ModelSerializer):
    name_model_name= serializers.SerializerMethodField()
    name_parameter= serializers.SerializerMethodField()
    name_unit= serializers.SerializerMethodField()
    class Meta:
        model = ModelStructure
        fields = ("id", "model_name", "parameter", "note","name_model_name","name_parameter","name_unit")
    
    def get_name_model_name(self, obj):
            model_name = obj.model_name
            if model_name: 
                result = f"{obj.model_name.name}"
            else:
                result = "" 
            return result
    def get_name_parameter(self, obj):
            parameter = obj.parameter
            result = f"{obj.parameter.name}"
            return result
    def get_name_unit(self, obj):
        parameter = obj.parameter
        if parameter.unit: 
            result = f"{parameter.unit.name}"
        else:
            result = ""  
        return result

class ResultSerializer(serializers.ModelSerializer):
    name_model_structure= serializers.SerializerMethodField()
    name_parameter = serializers.SerializerMethodField()
    name_unit = serializers.SerializerMethodField()
    class Meta:
        model = Result
        fields = ("id", "model_structure", "value", "upper_value", "lower_value", "note","name_model_structure","name_parameter","name_unit")

    def get_name_model_structure(self, obj):
            model_structure = obj.model_structure
            if model_structure.model_name:
                result = f"{obj.model_structure.model_name.name} "
            else:
                result = "" 
            return result
        
    def get_name_parameter(self, obj):
            model_structure = obj.model_structure
            result = f"{obj.model_structure.parameter.name}"
            return result
    def get_name_unit(self, obj):
        model_structure = obj.model_structure
        if model_structure.parameter.unit:
            result = f"{model_structure.parameter.unit.name}"
        else:
            result = ""  
        return result
        
        
class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("id", "name", "full_name", "url", "note")





class DataSetSerializer(serializers.ModelSerializer):
    name_result= serializers.SerializerMethodField()
    name_сlinical_сase = serializers.SerializerMethodField()
    name_source = serializers.SerializerMethodField()
    
    

    class Meta:
        model = DataSet
        fields = ("id", "result", "сlinical_сase","name_сlinical_сase", "source", "note","name_result","name_source")
        
    
    def get_name_result(self, obj):
        result = obj.result
        
        model_name = result.model_structure.model_name.name if result.model_structure.model_name else "Неизвестная модель"
        parameter_name = result.model_structure.parameter.name if result.model_structure.parameter else "Без параметра"
        unit_name = result.model_structure.parameter.unit.name if result.model_structure.parameter and result.model_structure.parameter.unit else ""
        resultA = f"{model_name} {parameter_name}={result.value}({result.lower_value}-{result.upper_value})"
        
        if unit_name:
            resultA += f" ({unit_name})"
        
        return resultA.strip()  

    def get_name_сlinical_сase(self, obj):
            сlinical_сase = obj.сlinical_сase
            result = f"{obj.сlinical_сase}"
            return result
    def get_name_source(self, obj):
            source = obj.source
            result = f"{obj.source}"
            return result

# class DataSetsSerializer(serializers.ModelSerializer):
#     name_result= serializers.SerializerMethodField()
    
#     name_source = serializers.SerializerMethodField()
    
    

#     class Meta:
#         model = DataSet
#         fields = ("name_result","name_source")
        
    
#     def get_name_result(self, obj):
#             result = obj.result
#             resultA = f"{obj.result.model_structure.model_name.name} {obj.result.model_structure.parameter.name}={obj.result.value}({obj.result.lower_value}-{obj.result.upper_value})({obj.result.model_structure.parameter.unit.name})"
#             return resultA
#     def get_name_source(self, obj):
#             source = obj.source
#             result = f"{obj.source}"
#             return result
           
class ClinicalCaseSerializer(serializers.ModelSerializer):
    datasets_source_name = serializers.SerializerMethodField()
    datasets_source_url = serializers.SerializerMethodField()
    datasets_result_value= serializers.SerializerMethodField()
    datasets_result_upper_value = serializers.SerializerMethodField()
    datasets_result_lower_value = serializers.SerializerMethodField()
    datasets_result_note = serializers.SerializerMethodField()
    datasets_result_model_structure_name = serializers.SerializerMethodField()
    datasets_result_model_structure_parameter = serializers.SerializerMethodField()
    
    name_location = serializers.SerializerMethodField()
    name_diagnosis = serializers.SerializerMethodField()
    name_complication = serializers.SerializerMethodField()
    name_stage = serializers.SerializerMethodField()
    name_risk_group = serializers.SerializerMethodField()
    name_radiation_therapy_type = serializers.SerializerMethodField()
    name_tumor = serializers.SerializerMethodField()
    name_node = serializers.SerializerMethodField()
    name_metastasis = serializers.SerializerMethodField()
    name_histology = serializers.SerializerMethodField()
    name_grade = serializers.SerializerMethodField()
    gender_display = serializers.SerializerMethodField()
    сlinical_сase_text= serializers.SerializerMethodField()
    
    text_location = serializers.SerializerMethodField()
    text_diagnosis = serializers.SerializerMethodField()
    text_complication = serializers.SerializerMethodField()
    text_stage = serializers.SerializerMethodField()
    text_risk_group = serializers.SerializerMethodField()
    text_radiation_therapy_type = serializers.SerializerMethodField()
    text_tumor = serializers.SerializerMethodField()
    text_node = serializers.SerializerMethodField()
    text_metastasis = serializers.SerializerMethodField()
    text_histology = serializers.SerializerMethodField()
    text_grade = serializers.SerializerMethodField()
   
    
    class Meta:
        model = ClinicalCase
        fields = (
            "id", "age", "age_min","age_max","quantity","gender","diagnosis", "refined_diagnosis", "spec_location",
            "complication", "stage", "risk_group", "radiation_therapy_type",
            "number_of_fractions", "single_dose", "treatment_duration", 
            "histology", "grade", "tumor", "node", "metastasis", "note",
            "name_location", "name_diagnosis", "name_complication", 
            "name_stage", "name_risk_group", "name_radiation_therapy_type", 
            "name_tumor", "name_node", "name_metastasis", "name_histology", 
            "name_grade", "gender_display","сlinical_сase_text","text_location", "text_diagnosis", "text_complication", "text_stage", "text_risk_group", "text_radiation_therapy_type", "text_tumor", "text_node", "text_metastasis", "text_histology", "text_grade"
            ,"datasets_source_name","datasets_source_url","datasets_result_value",
            "datasets_result_upper_value", 
            "datasets_result_lower_value", 
            "datasets_result_note", 
            "datasets_result_model_structure_name","datasets_result_model_structure_parameter"
            )

    def get_сlinical_сase_text(self, obj):
        return f"{obj}"
    def get_name_location(self, obj):
        return obj.spec_location.name if obj.spec_location else None

    def get_name_diagnosis(self, obj):
        return obj.diagnosis.code if obj.diagnosis else None

    def get_name_complication(self, obj):
        return obj.complication.name if obj.complication else None

    def get_name_stage(self, obj):
        return obj.stage.name if obj.stage else None

    def get_name_risk_group(self, obj):
        return obj.risk_group.name if obj.risk_group else None

    def get_name_radiation_therapy_type(self, obj):
        return obj.radiation_therapy_type.name if obj.radiation_therapy_type else None

    def get_name_tumor(self, obj):
        return obj.tumor.short_name if obj.tumor else None

    def get_name_node(self, obj):
        return obj.node.short_name if obj.node else None

    def get_name_metastasis(self, obj):
        return obj.metastasis.short_name if obj.metastasis else None

    def get_name_histology(self, obj):
        return obj.histology.name if obj.histology else None

    def get_name_grade(self, obj):
        return obj.grade.name if obj.grade else None

    def get_gender_display(self, obj):
        return obj.get_gender_display() if obj.gender is not None else None
   
    
    def get_text_location(self, obj):
        return f"{obj.spec_location}" if obj.spec_location else None

    def get_text_diagnosis(self, obj):
        return f"{obj.diagnosis}" if obj.diagnosis else None

    def get_text_complication(self, obj):
        return f"{obj.complication}" if obj.complication else None

    def get_text_stage(self, obj):
        return f"{obj.stage}" if obj.stage else None

    def get_text_risk_group(self, obj):
        return f"{obj.risk_group}" if obj.risk_group else None

    def get_text_radiation_therapy_type(self, obj):
        return f"{obj.radiation_therapy_type}" if obj.radiation_therapy_type else None

    def get_text_tumor(self, obj):
        return f"{obj.tumor}" if obj.tumor else None

    def get_text_node(self, obj):
        return f"{obj.node}" if obj.node else None

    def get_text_metastasis(self, obj):
        return f"{obj.metastasis}" if obj.metastasis else None

    def get_text_histology(self, obj):
        return f"{obj.histology}" if obj.histology else None

    def get_text_grade(self, obj):
        return f"{obj.grade}" if obj.grade else None    
    
    def get_datasets_source_name(self, obj):
        return [
            dataset.source.name if dataset.source else None
            for dataset in obj.dataset_set.all()
        ]
    def get_datasets_source_url(self, obj):
        return [
             dataset.source.url if dataset.source else None
            for dataset in obj.dataset_set.all()
        ]
    def get_datasets_result_value(self, obj):
        return [
           
                
                     dataset.result.value if dataset.result else None
                
            
            for dataset in obj.dataset_set.all()
        ] 
    def get_datasets_result_upper_value(self, obj):
        return [
            dataset.result.upper_value if dataset.result else None
            for dataset in obj.dataset_set.all()
        ]

    def get_datasets_result_lower_value(self, obj):
        return [
            dataset.result.lower_value if dataset.result else None
            for dataset in obj.dataset_set.all()
        ]

    def get_datasets_result_note(self, obj):
        return [
            dataset.result.note if dataset.result else None
            for dataset in obj.dataset_set.all()
        ]

    def get_datasets_result_model_structure_name(self, obj):
        return [
            (
                dataset.result.model_structure.model_name.name 
                if dataset.result and 
                dataset.result.model_structure and 
                dataset.result.model_structure.model_name 
                else "Неизвестная модель"
            ) 
            for dataset in obj.dataset_set.all()
        ]
        
    
    def get_datasets_result_model_structure_parameter(self, obj):
        return [
            dataset.result.model_structure.parameter.name if dataset.result else None 
            for dataset in obj.dataset_set.all()
        ]   
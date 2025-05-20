from django.contrib import admin


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
    ClinicalCaseComplication  
)


admin.site.register(Location)
admin.site.register(SpecLocation)
admin.site.register(Diagnosis)
admin.site.register(ClinicalCase)
admin.site.register(Unit)
admin.site.register(Parameter)
admin.site.register(ModelName)
admin.site.register(Stage)
admin.site.register(RiskGroup)
admin.site.register(Complication)
admin.site.register(ModelStructure)
admin.site.register(Result)
admin.site.register(Source)
admin.site.register(DataSet)
admin.site.register(RadiationTherapyType)
admin.site.register(Histology)
admin.site.register(Grade)
admin.site.register(Tumor)
admin.site.register(Node)
admin.site.register(Metastasis)
admin.site.register(ClinicalCaseComplication)

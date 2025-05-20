from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(prefix="radiation-therapy-type",viewset=views.RadiationTherapyTypeViewSet,basename="radiation-therapy-type",
)
router.register(prefix="location", viewset=views.LocationViewSet, basename="location")
router.register(prefix="spec-location", viewset=views.SpecLocationViewSet, basename="spec-location"
)

router.register(prefix="diagnosis", viewset=views.DiagnosisViewSet, basename="diagnosis"
)
router.register(prefix="clinical-case", viewset=views.ClinicalCaseViewSet, basename="clinical-case"
)
router.register(prefix="unit", viewset=views.UnitViewSet, basename="unit")
router.register(prefix="parameter", viewset=views.ParameterViewSet, basename="parameter"
)
router.register(prefix="model-name", viewset=views.ModelNameViewSet, basename="model-name"
)
router.register(prefix="stage", viewset=views.StageViewSet, basename="stage")
router.register(prefix="risk-group", viewset=views.RiskGroupViewSet, basename="risk-group"
)
router.register(prefix="complication", viewset=views.ComplicationViewSet, basename="complication"
)
router.register(prefix="сlinical-сase-сomplication", viewset=views.ClinicalCaseComplicationViewSet, basename="сlinical-сase-сomplication"
)

router.register(prefix="model-structure",viewset=views.ModelStructureViewSet,basename="model-structure",
)
router.register(prefix="result", viewset=views.ResultViewSet, basename="result")
router.register(prefix="source", viewset=views.SourceViewSet, basename="source")

router.register(prefix="dataset", viewset=views.DataSetViewSet, basename="dataset")
router.register(
    prefix="histology", viewset=views.HistologyViewSet, basename="histology"
)
router.register(prefix="grade", viewset=views.GradeViewSet, basename="grade")
router.register(prefix="tumor", viewset=views.TumorViewSet, basename="tumor")
router.register(prefix="node", viewset=views.NodeViewSet, basename="node")
router.register(
    prefix="metastasis", viewset=views.MetastasisViewSet, basename="metastasis"
)

urlpatterns = [
    path("", include(router.urls)),
]

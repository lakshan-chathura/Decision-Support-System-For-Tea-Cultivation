from django.urls import path
from research_dss_app import views

urlpatterns = [
    path('maps/<str:operation>',views.RGBAndNIRMapView.as_view(),name="RGB and NIR"),
    path('maps/ndvi/',views.NDVIMapView.as_view(),name="NDVI"),
    path('maps/rgb/analyze/',views.TeaBudIdentificationView.as_view(),name="Tea bud identification"),
    path('data/field/',views.FieldVisitView.as_view(),name="Field visit"),
    path('maps/tiles/create/',views.TilerView.as_view(),name="Tiler"),
    path('images/upload/<str:real_name>/<str:mode>',views.FieldVisitView.as_view(),name="Image upload"),
    path('project/setup/',views.TilerView.as_view(),name="Project setup")
]

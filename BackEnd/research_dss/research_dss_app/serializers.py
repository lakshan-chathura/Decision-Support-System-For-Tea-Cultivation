from research_dss_app.models import FieldVisit,PlantHealth
from rest_framework import serializers

class FieldVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldVisit
        fields = '__all__'

class PlantHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantHealth
        fields = '__all__'

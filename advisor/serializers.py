from rest_framework import serializers
from .models import Plant, Disease, Treatment


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'


class DiseaseSerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)

    class Meta:
        model = Disease
        fields = '__all__'


class PlantSerializer(serializers.ModelSerializer):
    diseases = DiseaseSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = '__all__'
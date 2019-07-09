from rest_framework import serializers
from ford3.models.field_of_study import FieldOfStudy


class FieldOfStudySerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldOfStudy
        fields = ['name']

from rest_framework import serializers
from ford3.models.subject import Subject
from api.serializers.secondary_institution_type import SecondaryInstitutionTypeSerializer  # noqa


class SubjectSerializer(serializers.ModelSerializer):
    secondary_institution_types = SecondaryInstitutionTypeSerializer(many=True)

    class Meta:
        model = Subject
        fields = '__all__'

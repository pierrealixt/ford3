from rest_framework import serializers
from ford3.models.secondary_institution_type import SecondaryInstitutionType


class SecondaryInstitutionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecondaryInstitutionType
        fields = '__all__'

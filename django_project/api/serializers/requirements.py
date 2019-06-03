from rest_framework import serializers
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel
from ford3.models.requirement import Requirement
from api.serializers.utilities.fields import EnumField


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'

    min_nqf_level = EnumField(enum=SaqaQualificationLevel)

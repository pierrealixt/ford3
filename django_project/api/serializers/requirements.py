from rest_framework import serializers
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel
from ford3.models.requirement import Requirement
from api.serializers.utilities.enum_field import EnumField


class RequirementSerializer(serializers.ModelSerializer):
    min_nqf_level = EnumField(enum=SaqaQualificationLevel)
    subjects = serializers.SerializerMethodField()

    def get_subjects(self, obj):
        if obj.require_certain_subjects:
            return obj.qualification.entrance_req_subjects_list
        else:
            return []

    class Meta:
        model = Requirement
        fields = '__all__'

from rest_framework import serializers
from ford3.models.qualification import Qualification
from api.serializers.qualification_event import QualificationEventSerializer
from api.serializers.subject import SubjectSerializer
from api.serializers.saqa_qualification import SAQAQualificationSerializer
from api.serializers.occupation import OccupationSerializer
from api.serializers.interest import InterestSerializer
from api.serializers.requirements import RequirementSerializer
from api.serializers.utilities.common_excluded_fields import CommonExcludedFields  # noqa


class QualificationSerializer(serializers.ModelSerializer):
    qualification_events = QualificationEventSerializer(many=True)
    saqa_qualification = SAQAQualificationSerializer()
    occupations = OccupationSerializer(many=True)
    interests = InterestSerializer(many=True)
    requirement = RequirementSerializer()
    campus = serializers.StringRelatedField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Qualification
        exclude = CommonExcludedFields.user_details + ['completion_rate']

    def get_name(self, obj):
        return obj.saqa_qualification.name

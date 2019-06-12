from rest_framework import serializers
from ford3.models.campus import Campus
from api.serializers.campus_event import CampusEventSerializer
from api.serializers.qualification import QualificationSerializer
from api.serializers.utilities.common_excluded_fields import CommonExcludedFields  # noqa


class CampusSerializer(serializers.ModelSerializer):
    """
    This is the campus serializer
    """
    campus_events = CampusEventSerializer(many=True)
    qualification_set = QualificationSerializer(many=True)

    class Meta:
        model = Campus
        exclude = CommonExcludedFields.user_details

from rest_framework import serializers
from ford3.models.qualification_event import QualificationEvent
from api.serializers.utilities.common_excluded_fields import CommonExcludedFields  # noqa


class QualificationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualificationEvent
        exclude = ['qualification']

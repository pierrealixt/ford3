from rest_framework import serializers
from ford3.models.campus_event import CampusEvent
from api.serializers.utilities.common_excluded_fields import CommonExcludedFields  # noqa


class CampusEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampusEvent
        exclude = CommonExcludedFields.common

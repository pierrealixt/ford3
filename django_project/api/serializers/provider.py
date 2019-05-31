from rest_framework import serializers
from ford3.models.provider import Provider
from api.serializers.campus import CampusSerializer
from api.serializers.utilities.common_excluded_fields import CommonExcludedFields  # noqa


class ProviderSerializer(serializers.ModelSerializer):
    campus = CampusSerializer(many=True)

    class Meta:
        model = Provider
        exclude = CommonExcludedFields.user_details

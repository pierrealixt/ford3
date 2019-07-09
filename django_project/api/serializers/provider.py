from rest_framework import serializers
from ford3.models.provider import Provider
from api.serializers.campus import CampusSerializer
from api.serializers.utilities.common_excluded_fields import CommonExcludedFields  # noqa
from ford3.models.campus import Campus
from ford3.location import location_as_dict


class ProviderSerializer(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField()
    province = serializers.StringRelatedField()
    location = serializers.SerializerMethodField()

    def get_campus(self, obj):
        queryset = list(Campus.active_objects.filter(provider_id=obj.id).all())
        serializer = CampusSerializer(
            many=True, read_only=True, instance=queryset)
        return serializer.data

    def get_location(self, obj):
        try:
            return location_as_dict(str(obj.location))
        except:
            return None


    class Meta:
        model = Provider
        exclude = CommonExcludedFields.user_details

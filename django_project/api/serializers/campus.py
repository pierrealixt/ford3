from rest_framework import serializers
from ford3.models.campus import Campus
from api.serializers.campus_event import CampusEventSerializer
from api.serializers.qualification import QualificationSerializer
from api.serializers.utilities.common_excluded_fields import CommonExcludedFields  # noqa
from ford3.models.qualification import Qualification
from ford3.location import location_as_dict


class CampusSerializer(serializers.ModelSerializer):
    """
    This is the campus serializer
    """
    campus_events = CampusEventSerializer(many=True)
    published_qualifications = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_published_qualifications(self, obj):
        queryset = list(Qualification.published_objects.filter(
            campus_id=obj.id).all())
        serializer = QualificationSerializer(
            many=True, read_only=True, instance=queryset)
        return serializer.data

    def get_location(self, obj):
        try:
            return location_as_dict(str(obj.location))
        except:
            return None


    class Meta:
        model = Campus
        exclude = CommonExcludedFields.user_details

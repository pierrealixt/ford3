from rest_framework import viewsets
from ford3.models.campus import Campus
from api.serializers.campus import CampusSerializer


class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return all details for a campus specified by ID.

    list:
    Returns a list of all campuses registered with OpenEdu.

    """

    serializer_class = CampusSerializer

    def get_queryset(self):
        return Campus.active_objects.all()

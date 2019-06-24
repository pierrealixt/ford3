from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = (
        'provider',
        'name',
        'telephone',
        'email',
        'max_students_per_year',
        'physical_address_city')
    ordering_fields = (
        'name',
        'id',
        'max_students_per_year',
        'physical_address_city')

    def get_queryset(self):
        return Campus.active_objects.all()

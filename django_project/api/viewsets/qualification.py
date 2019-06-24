from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ford3.models.qualification import Qualification
from api.serializers.qualification import QualificationSerializer


class QualificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return all details for a qualification registered with OpenEdu
    specified by ID.

    list:
    Returns a list of all qualifications registered with OpenEdu.
    """
    serializer_class = QualificationSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = (
        'name',
        'campus',
        'saqa_qualification',
        'short_description',
        'long_description',
        'duration',
        'full_time',
        'credits_after_completion',
        'distance_learning',
        'completion_rate',
        'total_cost',
        'critical_skill',
        'green_occupation',
        'high_demand_occupation'
    )
    ordering_fields = ('name', 'id', 'total_cost')

    def get_queryset(self):
        return Qualification.published_objects.all()

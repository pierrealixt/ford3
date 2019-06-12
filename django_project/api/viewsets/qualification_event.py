from rest_framework import viewsets
from ford3.models.qualification_event import QualificationEvent
from api.serializers.qualification_event import QualificationEventSerializer


class QualificationEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return a qualification event for a given ID.

    version:
    This value should be set to 1.
    """
    queryset = QualificationEvent.objects.all()
    serializer_class = QualificationEventSerializer

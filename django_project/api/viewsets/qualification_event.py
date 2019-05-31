from rest_framework import viewsets
from ford3.models.qualification_event import QualificationEvent
from api.serializers.qualification_event import QualificationEventSerializer


class QualificationEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QualificationEvent.objects.all()
    serializer_class = QualificationEventSerializer

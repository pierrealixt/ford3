from rest_framework import viewsets
from ford3.models.campus_event import CampusEvent
from api.serializers.campus_event import CampusEventSerializer


class CampusEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CampusEvent.active_objects.all()
    serializer_class = CampusEventSerializer

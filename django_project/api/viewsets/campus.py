from rest_framework import viewsets
from ford3.models.campus import Campus
from api.serializers.campus import CampusSerializer


class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campus.active_objects.all()
    serializer_class = CampusSerializer

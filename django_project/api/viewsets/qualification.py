from rest_framework import viewsets
from ford3.models.qualification import Qualification
from api.serializers.qualification import QualificationSerializer


class QualificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Qualification.active_objects.all()
    serializer_class = QualificationSerializer

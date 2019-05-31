from rest_framework import viewsets
from ford3.models.saqa_qualification import SAQAQualification
from api.serializers.saqa_qualification import SAQAQualificationSerializer


class SAQAQualificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SAQAQualification.objects.all()
    serializer_class = SAQAQualificationSerializer

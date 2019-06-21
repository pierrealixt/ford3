from rest_framework import viewsets
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

    def get_queryset(self):
        return Qualification.published_objects.all()

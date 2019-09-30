from rest_framework import viewsets
from ford3.models.occupation import Occupation
from api.serializers.occupation import OccupationNameSerializer


class OccupationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all occupations.
    """

    queryset = Occupation.objects.all()
    serializer_class = OccupationNameSerializer

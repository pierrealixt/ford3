from rest_framework import viewsets
from ford3.models.interest import Interest
from api.serializers.interest import InterestSerializer


class InterestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Returns a list of all interests.
    """

    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

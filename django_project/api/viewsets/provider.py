from rest_framework import viewsets
from ford3.models.provider import Provider
from api.serializers.provider import ProviderSerializer


class ProvidersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Provider.active_objects.all()
    serializer_class = ProviderSerializer

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ford3.models.provider import Provider
from api.serializers.provider import ProviderSerializer


class ProvidersViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return all details associated with a provider.

    list:
    Returns a list of all providers registered with OpenEdu.
    """
    queryset = Provider.active_objects.all()
    serializer_class = ProviderSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = (
        'name',
        'provider_type',
        'telephone',
        'website',
        'email',
        'admissions_contact_no',
        'province',
        'physical_address_city')
    ordering_fields = (
        'name',
        'id',
        'provider_type',
        'province',
        'physical_address_city')

from django.http import JsonResponse
from ford3.models.occupation import Occupation


def index(request):
    query = request.GET.get('q', None)
    if len(query) == 1:
        results = list(Occupation.objects.filter(
            name__startswith=query).values('id', 'name'))
    else:
        results = list(Occupation.objects.filter(
            name__icontains=query).values('id', 'name'))

    return JsonResponse({'results': results})

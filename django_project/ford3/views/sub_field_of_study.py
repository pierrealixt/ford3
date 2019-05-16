from django.http import JsonResponse
from ford3.models.sub_field_of_study import SubFieldOfStudy


def index(request, fos_id):
    sfos = SubFieldOfStudy.objects.filter(
        field_of_study_id=fos_id).values('id', 'name')
    return JsonResponse({'results': list(sfos)})

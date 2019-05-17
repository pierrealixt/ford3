import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from ford3.models.saqa_qualification import SAQAQualification
from ford3.models.field_of_study import FieldOfStudy


def json_response(results):
    return JsonResponse({'results': results})


def search(request):
    if request.method != 'GET':
        return json_response([])

    query = request.GET.get('q', None)

    if query is None or len(query) == 0:
        return json_response([])

    results = SAQAQualification.search(query)

    return json_response(results)


def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    try:
        data = json.loads(request.body)['saqa_qualification']
        saqa_qualification = SAQAQualification.create_non_accredited(data)

    except ValidationError as ve:
        return JsonResponse({
            'success': False,
            'error': ';'.join(ve.messages)})

    except FieldOfStudy.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Field of Study is invalid.'})

    except MultiValueDictKeyError:
        return HttpResponseBadRequest()

    return JsonResponse({
        'success': True,
        'saqa_qualification': saqa_qualification.as_dict()})

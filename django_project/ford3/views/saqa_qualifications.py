import json
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from ford3.models import (
    Provider,
    SAQAQualification
)


def json_response(results):
    return HttpResponse(
        json.dumps({
            'results': results}),
        content_type='application/json')


def search(request):
    if request.method != 'GET':
        return json_response([])

    query = request.GET.get('q', None)

    if query is None or len(query) == 0:
        return json_response([])

    results = SAQAQualification.search(query)

    return json_response(results)


def create(request):
    
    provider = Provider.objects.get(pk=request.POST['provider_id'])
    
    try:
        saqa_qualification = SAQAQualification.create_non_accredited(
            name=request.POST['saqa_qualification_name'],
            creator_provider=provider)
    except ValidationError as ve:
        return HttpResponse(
            json.dumps({
                'success': False,
                'error': ';'.join(ve.messages)}),
            content_type='application/json')        

    return HttpResponse(
        json.dumps({
            'success': True,
            'saqa_qualification': saqa_qualification.as_dict()}),
        content_type='application/json')

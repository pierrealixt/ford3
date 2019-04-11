import json
from django.shortcuts import (
    render,
    get_object_or_404,
    render_to_response
)
from django.http import HttpResponse
from ford3.models import (
    Campus,
    Qualification,
    SAQAQualification
)


def json_response(results):
    return HttpResponse(
        json.dumps({
            'results': results}),
        content_type='application/json')


def saqa_qualifications(request):
    if request.method != 'GET':
        return json_response([])

    query = request.GET.get('q', None)

    if query is None or len(query) == 0:
        return json_response([])

    results = SAQAQualification.search(query)

    return json_response(results)


def show_campus(request, provider_id, campus_id):
    campus = get_object_or_404(
        Campus,
        id=campus_id)
    form_data = {
        'provider_name': campus.provider.name
    }
    context = {
        'form_data': form_data,
        'campus': campus,
        'provider': campus.provider
    }
    return render(request, 'campus.html', context)


def show_qualification(request, provider_id, campus_id, qualification_id):
    qualification = get_object_or_404(
        Qualification,
        id=qualification_id)
    context = {
        'qualification': qualification,
        'provider': qualification.campus.provider
    }
    return render(request, 'qualification.html', context)


def widget_examples(request):
    return render_to_response('test_widgets.html')

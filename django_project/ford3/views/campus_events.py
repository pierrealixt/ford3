import json
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from ford3.models.campus_event import CampusEvent
from ford3.models.campus import Campus


def create(request, campus_id):
    new_campus_event = CampusEvent()

    new_campus_event.name = request.POST['name']
    new_campus_event.date_start = request.POST['date_start']
    new_campus_event.date_end = request.POST['date_end']
    new_campus_event.http_link = request.POST['http_link']
    new_campus_event.campus = Campus.objects.get(pk=campus_id)
    try:
        new_campus_event.full_clean()
        new_campus_event.save()
        response = json.dumps({
            'success': True,
            'campus_event': model_to_dict(new_campus_event)
        })
    except ValidationError:
        response = json.dumps({'success': False})

    return HttpResponse(response)

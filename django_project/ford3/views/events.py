import json
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from ford3.models.campus_event import CampusEvent
from ford3.models.campus import Campus
from ford3.models.qualification_event import QualificationEvent
from ford3.models.qualification import Qualification
from ford3.views.wizard_utilities import add_http_to_link


def create_or_update(request, owner_id, event_type):
    if 'id' in request.POST:
        return update(request, event_type)
    else:
        return create(request, owner_id, event_type)


def update(request, event_type):
    if event_type == 'campus':
        event_to_update = (CampusEvent.objects.get(pk=request.POST['id']))
    elif event_type == 'qualification':
        event_to_update = (
            QualificationEvent.objects.get(pk=request.POST['id']))
    try:
        event_to_update.name = request.POST['name']
        event_to_update.date_start = request.POST['date_start']
        event_to_update.date_end = request.POST['date_end']
        event_to_update.http_link = add_http_to_link(request.POST['http_link'])
        event_to_update.full_clean()
        event_to_update.save()
        event_to_update_dict = (
            get_event_dictionary(event_to_update))
        response = json.dumps({
            'success': True,
            'event': event_to_update_dict
        })
    except ValidationError as error:
        response = json.dumps({
            'success': False,
            'error_msg': ''.join(error.messages)
        })

    return HttpResponse(response)


def create(request, owner_id, event_type):
    if event_type == 'campus':
        new_event = CampusEvent()
        new_event.campus = Campus.objects.get(pk=owner_id)
    elif event_type == 'qualification':
        new_event = QualificationEvent()
        new_event.qualification = Qualification.objects.get(pk=owner_id)
    new_event.name = request.POST['name']
    new_event.date_start = request.POST['date_start']
    new_event.date_end = request.POST['date_end']
    new_event.http_link = request.POST['http_link']

    try:
        new_event.full_clean()
        new_event.save()
        new_event_dict = get_event_dictionary(new_event)
        response = json.dumps({
            'success': True,
            'event': new_event_dict,
        })
    except ValidationError as error:
        response = json.dumps({
            'success': False,
            'error_msg': error.messages
        })

    return HttpResponse(response)


def get_event_dictionary(event):
    new_event_dict = {
        'id': event.id,
        'name': event.name,
        'date_start': str(event.date_start),
        'date_end': str(event.date_end),
        'http_link': event.http_link
    }
    return new_event_dict


def delete(request, event_type):
    try:
        event_id = request.POST['id']
        if event_type == 'campus':
            CampusEvent.objects.get(pk=event_id).soft_delete()
        elif event_type == 'qualification':
            QualificationEvent.objects.get(pk=event_id).delete()
        response = json.dumps({'success': True})
    except KeyError:
        response = json.dumps({
            'success': False,
            'error_msg': 'ID missing from request'
        })
    return HttpResponse(response)

import json
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from ford3.models.campus_event import CampusEvent
from ford3.models.campus import Campus


def create_or_update(request, campus_id):

    if 'id' in request.POST:
        return update(request)
    else:
        return create(request, campus_id)


def update(request):
    campus_event_to_update: CampusEvent = (
        CampusEvent.objects.get(pk=request.POST['id']))
    if campus_event_to_update:
        try:
            campus_event_to_update.name = request.POST['name']
            campus_event_to_update.date_start = request.POST['date_start']
            campus_event_to_update.date_end = request.POST['date_end']
            campus_event_to_update.http_link = request.POST['http_link']
            campus_event_to_update.full_clean()
            campus_event_to_update.save()
            campus_event_to_update_dict = (
                get_campus_event_dictionary(campus_event_to_update))
            response = json.dumps({
                'success': True,
                'campus_event': campus_event_to_update_dict
            })
        except ValidationError as error:
            response = json.dumps({
                'success': False,
                'error_msg': ''.join(error.messages)
            })

    return HttpResponse(response)


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
        new_campus_event_dict = get_campus_event_dictionary(new_campus_event)
        response = json.dumps({
            'success': True,
            'campus_event': new_campus_event_dict,
        })
    except ValidationError as error:
        response = json.dumps({
            'success': False,
            'error_msg': error.messages
        })

    return HttpResponse(response)


def get_campus_event_dictionary(campus_event):
    new_campus_event_dict = {
        'id': campus_event.id,
        'name': campus_event.name,
        'date_start': str(campus_event.date_start),
        'date_end': str(campus_event.date_end),
        'http_link': campus_event.http_link
    }
    return new_campus_event_dict


def delete(request):
    try:
        event_id = request.POST['id']
        CampusEvent.objects.get(pk=event_id).soft_delete()
        response = json.dumps({'success': True})
    except KeyError:
        response = json.dumps({
            'success': False,
            'error_msg': 'ID missing from request'
        })
    return HttpResponse(response)

from django.shortcuts import (
    render,
    get_object_or_404,
    render_to_response,
    redirect,
    reverse
)
from django.http.response import HttpResponse
from ford3.models.qualification import (
    Qualification
)
from ford3.decorators import provider_check, campus_check, qualification_check


@provider_check
@campus_check
@qualification_check
def show_qualification(request, provider_id, campus_id, qualification_id):
    qualification = get_object_or_404(
        Qualification,
        id=qualification_id)
    context = {
        'qualification': qualification,
        'provider': qualification.campus.provider,
        # make sure logo has been uploaded before set the context
        # otherwise, let it empty
        'provider_logo':
            qualification.campus.provider.provider_logo.url
            if qualification.campus.provider.provider_logo else ""
    }
    return render(request, 'qualification.html', context)


@provider_check
@campus_check
@qualification_check
def delete_qualification(request, provider_id, campus_id, qualification_id):
    qualification = get_object_or_404(
        Qualification,
        id=qualification_id)

    qualification.deleted = True
    qualification.save()

    return redirect(reverse('dashboard'))


def import_qualification(request, provider_id):
    import json
    from ford3.import_qualifications import import_excel_data

    row = json.loads(request.body)

    success, errors = import_excel_data(row)

    context = {
        'result': {
            'success': success,
            'errors': errors
        }
    }
    return HttpResponse(
        json.dumps(context),
        content_type="application/json")

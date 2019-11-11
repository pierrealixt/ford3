from django.shortcuts import (
    render,
    get_object_or_404,
    render_to_response,
    redirect,
    reverse
)
import json
import decimal
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
    if 'headers' in request.GET:
        #  Build definition
        pass
    row = json.loads(request.body)

    success, errors, diffs = import_excel_data(row)

    context = {
        'result': {
            'success': success,
            'errors': errors,
            'diffs': diffs,

        }
    }
    response_string = json.dumps(context, cls=DecimalEncoder)
    return HttpResponse(
        response_string,
        content_type="application/json")


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)
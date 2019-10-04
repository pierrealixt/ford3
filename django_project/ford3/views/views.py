from django.shortcuts import (
    render,
    get_object_or_404,
    render_to_response,
    redirect,
    reverse
)
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


from ford3.models.campus import Campus
from ford3.models.saqa_qualification import SAQAQualification

# @login_required()
# @require_http_methods(['POST'])

def diff(key, obj, new_value):
    if getattr(obj, key) != new_value:
        setattr(obj, key, new_value)
        obj.save()
        return True
    return False


def import_qualification(request, provider_id):
    import json
    data = json.loads(request.body)
    try:
        campus = Campus.objects.get(
            name=data['campus_name'],
            provider_id=provider_id)

        qualification = campus.qualification_set.filter(
            deleted=False,
            saqa_qualification__saqa_id=data['saqa_qualification_id']
        )
        if len(qualification) == 0:
            pass
            # create qualification
        elif len(qualification) >= 1:
            qualification = qualification[0]
            report = {}
            qualification_keys = [
                key for key in data.keys()
                if key.split('_')[0] == 'qualification'
            ]
            for key in qualification_keys:
                report[key] = diff(
                    key[key.find('_') + 1:],
                    qualification,
                    data[key])
            import pdb; pdb.set_trace()



    except Campus.DoesNotExist:
        return 'campus_name does not belong to provider'






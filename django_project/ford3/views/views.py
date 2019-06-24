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


def widget_examples(request):
    return render_to_response('test_widgets.html')

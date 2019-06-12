from django.shortcuts import redirect, reverse, get_object_or_404
from ford3.models.qualification import Qualification


def toggle_publication(request, provider_id, qualification_id, campus_id):
    qualification = get_object_or_404(
        Qualification,
        pk=qualification_id)
    qualification.published = not qualification.published
    qualification.save()
    return redirect(reverse('show-campus',
                            args=[str(provider_id),
                                  str(campus_id)]))

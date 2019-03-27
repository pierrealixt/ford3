# coding=utf-8

from django.conf import settings
from django.shortcuts import render, redirect, render_to_response
from django.db import transaction, IntegrityError
from ford3.models.provider import Provider
from ford3.models.campus import Campus
from ford3.forms.provider_form import ProviderForm
from formtools.wizard.views import CookieWizardView


class CampusWizard(CookieWizardView):

    file_storage = settings.DEFAULT_FILE_STORAGE


@transaction.atomic
def provider_form(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            new_provider = Provider()
            provider_type = form.cleaned_data['provider_type']
            telephone = form.cleaned_data['telephone']
            email = form.cleaned_data['email']
            physical_address_line_1 = (
                form.cleaned_data['physical_address_line_1'])
            physical_address_line_2 = (
                form.cleaned_data['physical_address_line_2'])
            physical_address_city = form.cleaned_data['physical_address_city']
            postal_address = form.cleaned_data['postal_address']
            admissions_contact_no = form.cleaned_data['admissions_contact_no']
            new_provider.provider_type = provider_type
            new_provider.telephone = telephone
            new_provider.email = email
            new_provider.physical_address_line_1 = physical_address_line_1
            new_provider.physical_address_line_2 = physical_address_line_2
            new_provider.physical_address_city = physical_address_city
            new_provider.postal_address = postal_address
            new_provider.admissions_contact_no = admissions_contact_no
            new_provider.save()

            number_of_campuses = int(request.POST['number-of-campuses'])
            try:
                with transaction.atomic():
                    for idx in range(number_of_campuses):
                        campus_name = request.POST[f'campus_name_{idx +  1}']
                        Campus.objects.create(provider_id=new_provider,
                                              name=campus_name)
            except IntegrityError:
                return render(request, 'provider_form.html', {'form': form})
            return redirect('/')
    else:
        form = ProviderForm(initial={'name': 'False Bay College'})
    return render(request, 'provider_form.html', {'form': form})


def widget_examples(request):
    return render_to_response('test_widgets.html')

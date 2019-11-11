import io
import json
from datetime import datetime
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404)
from django.db import IntegrityError
from django.urls import reverse
from ford3.forms.provider_form import ProviderForm
from ford3.models.provider import Provider
from ford3.decorators import provider_check
from ford3.smart_excel.smart_excel import SmartExcel
from ford3.smart_excel.definition import (
    OPENEDU_EXCEL_DEFINITION
)
from ford3.smart_excel.data_model import (
    OpenEduSmartExcelData
)


@login_required()
@permission_required('ford3.add_provider', raise_exception=True)
@require_http_methods(['GET'])
def new(request):
    context = {
        'form': ProviderForm(),
        'is_new_provider': True,
        'submit_url': reverse('create-provider')
    }
    return render(
        request,
        'provider_form.html',
        context)


@login_required()
@permission_required('ford3.add_provider', raise_exception=True)
@require_http_methods(['POST'])
def create(request):
    form = ProviderForm(request.POST, request.FILES)

    if form.is_valid():
        provider = form.save(commit=False)
        try:
            provider.created_by = request.user
            provider.edited_by = request.user
            provider.save_location_data(request.POST)
            provider.save()
        except IntegrityError:
            form.initial = set_form_location(form.initial, request.POST)
            return render(request, 'provider_form.html', {'form': form})
        except ValidationError as ve:
            form.initial = set_form_location(form.initial, request.POST)
            context = {
                'provider_error': ''.join([
                    m_val[0]
                    for m_key, m_val
                    in ve.message_dict.items()]),
                'form': form
            }
            return render(request, 'provider_form.html', context)
        redirect_url = reverse(
            'show-provider',
            args=[str(provider.id)])
        return redirect(redirect_url)
    else:
        form.initial = set_form_location(form.initial, request.POST)
        context = {
            'form': form,
            'is_new_provider': True,
            'submit_url': reverse('create-provider')
        }
        return render(request, 'provider_form.html', context)


def set_form_location(form, post_data):
    try:
        form.update({
            'location_value_x': post_data['location_value_x'],
            'location_value_y': post_data['location_value_y']})
    except:
        form.update({
            'location_value_x': 0,
            'location_value_y': 0})
    return form


@login_required()
@permission_required('ford3.change_provider', raise_exception=True)
@require_http_methods(['GET'])
@provider_check
def edit(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id)
    form = ProviderForm(instance=provider)
    submit_url = reverse(
        'update-provider',
        args=[str(provider.id)])

    form.initial.update(provider.get_location_as_dict)

    context = {
        'form': form,
        'submit_url': submit_url
    }

    return render(
        request,
        'provider_form.html',
        context)


@login_required()
@permission_required('ford3.change_provider', raise_exception=True)
@require_http_methods(['POST'])
@provider_check
def update(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id)
    form = ProviderForm(request.POST, request.FILES, instance=provider)

    if form.is_valid():
        try:
            provider.save_location_data(request.POST)
            provider = form.save()
            provider.edited_by = request.user
            provider.save()
        except ValidationError as ve:
            context = {
                'provider_error': ''.join([
                    m_val[0]
                    for m_key, m_val
                    in ve.message_dict.items()]),
                'form': form
            }
            return render(request, 'provider_form.html', context)
        redirect_url = reverse(
            'show-provider',
            args=[str(provider.id)])
    else:
        submit_url = reverse(
            'update-provider',
            args=[str(provider.id)])
        context = {
            'form': form,
            'submit_url': submit_url
        }
        try:
            form.initial.update({
                'location_value_x': request.POST['location_value_x'],
                'location_value_y': request.POST['location_value_y']})
        except:
            form.initial.update({
                'location_value_x': 0,
                'location_value_y': 0})
        return render(
            request,
            'provider_form.html',
            context)

    return redirect(redirect_url)


@login_required
@require_http_methods(['GET'])
@provider_check
def show(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id
    )

    context = {
        'provider': provider
    }
    # make sure logo has been uploaded before set the context
    # otherwise, let it empty
    if provider.provider_logo:
        context['provider_logo'] = provider.provider_logo.url

    return render(request, 'provider.html', context)


@login_required()
@permission_required('ford3.delete_provider', raise_exception=True)
@require_http_methods(['GET'])
@provider_check
def delete(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id
    )

    provider.deleted = True
    provider.deleted_by = request.user
    provider.save()

    return redirect(reverse('dashboard'))


@login_required()
@require_http_methods(['GET'])
@provider_check
def dump(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id
    )

    filename = '{provider_name}_{date_today}.xlsx'.format(
        provider_name=provider.name,
        date_today=datetime.today().strftime('%Y-%m-%d')
    )

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename={filename}'.format(
        filename=filename
    )

    response.write(excel_dump(provider.id))
    return response


@login_required()
@require_http_methods(['POST'])
@provider_check
def upload(request, provider_id):
    provider = get_object_or_404(
        Provider,
        id=provider_id
    )

    try:
        data, columns = import_excel(request.FILES['excel'], provider.id)

    except Exception as e:
        context = {
            'error_upload': str(e),
            'provider': provider,
        }
        return render(request, 'provider.html', context)
    column_keys = []
    for column in columns:
        next_column = {'name': column['name'], 'key': column['key']}
        column_keys.append(next_column)
    context = {
        'data': json.dumps(data),
        'columns': json.dumps(column_keys),
        'provider': provider
    }
    return render(request, 'import.html', context)


def import_excel(file, provider_id):
    path = '/tmp/excel.xlsx'

    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    excel = SmartExcel(
        definition=OPENEDU_EXCEL_DEFINITION,
        data=OpenEduSmartExcelData(provider_id),
        path=path,
    )

    excel.parse()
    return excel.parsed_data, excel.columns


def excel_dump(provider_id):

    excel = SmartExcel(
        output=io.BytesIO(),
        definition=OPENEDU_EXCEL_DEFINITION,
        data=OpenEduSmartExcelData(provider_id)
    )

    excel.dump()
    return excel.output.getvalue()

# coding=utf-8
"""Views."""
# noinspection PyUnresolvedReferences
import logging
logger = logging.getLogger(__name__)

from django.views.generic import TemplateView, View
from django.shortcuts import render
from ford3.forms.prospect_form import ProspectForm
from ford3.models.prospect import Prospect


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prospect_form'] = ProspectForm()

        return context

    def post(self, request, *args, **kwargs):
        form = ProspectForm(request.POST)
        if form.is_valid():
            
            prospect = Prospect(
                name=form.cleaned_data['name'],
                telephone=form.cleaned_data['telephone'],
                email=form.cleaned_data['email'])
            
            prospect.save()

            return render(
                request, 
                self.template_name,
                {'form_submitted': True, 'prospect_form': ProspectForm(), 'prospect': prospect})
        else:
            return render(
                request,
                self.template_name,
                {'form_submitted': False, 'prospect_form': form})
    


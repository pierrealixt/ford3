# coding=utf-8
"""Views."""
# noinspection PyUnresolvedReferences
import logging
logger = logging.getLogger(__name__)

from django.views.generic import TemplateView

from ford3.forms.prospect_form import ProspectForm

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prospect_form'] = ProspectForm()
        return context

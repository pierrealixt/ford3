from django.test import TestCase
from ford3.forms.provider_form import ProviderForm, EMPTY_TEL_ERROR


class ProviderFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        EMPTY_MESSAGE_ERROR = 'This field is required.'
        form = ProviderForm(
            data={'provider_type' : '',
                  'telephone' : '',
                  'admissions_contact_no' : '',
                  'email' : '',
                  'website': '',
                  'physical_address_line_1' : '',
                  'physical_address_line_2' : '',
                  'physical_address_city': '',
                  'postal_address': '',
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['telephone'], [EMPTY_TEL_ERROR])
        self.assertEqual(form.errors['physical_address_line_1'],
                         [EMPTY_MESSAGE_ERROR])
        self.assertEqual(form.errors['physical_address_city'],
                         [EMPTY_MESSAGE_ERROR])
        self.assertEqual(form.errors['postal_address'],
                         [EMPTY_MESSAGE_ERROR])

    def test_provider_page_uses_provider_form(self):
        response = self.client.get('/ProviderForm/')
        self.assertIsInstance(response.context['form'], ProviderForm)

    def test_form_validation_for_max_length(self):
        form = ProviderForm(
            data={'telephone': '0821234123412341234',
                  'email': 'anemailwithouttheatsign',
                  'postal_address': '12345'})
        self.assertFalse(form.is_valid())
        try:
            self.assertIn('Ensure this value has at most 12 characters',
                          str(form.errors['telephone'][0]))
        except KeyError:
            self.fail(msg='No error raised for telephone field'
                          ' being too long.')
        try:
            self.assertIn('Ensure this value has at most 4 characters',
                          str(form.errors['postal_address'][0]))
        except KeyError:
            self.fail(msg='No error raised for postal_address field'
                          ' being too long.')

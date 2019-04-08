import unittest
from ford3.tests.functional.utils import SeleniumTestCase, selenium_flag_ready
from ford3.tests.models.model_factories import ModelFactories
from django.urls import reverse


class TestProviderForm(SeleniumTestCase):

    def setUp(self):
        self.new_provider = ModelFactories.get_provider_test_object()

    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def test_provider_form(self):

        # User has created a basic account and now needs to add
        # provider form details and have been redirected to the provider form.
        provider_form_url = reverse(
            'edit-provider',
            args=(str(self.new_provider.id)))

        self.driver.get(f'{self.live_server_url}{provider_form_url}')
        html = self.driver.page_source
        self.assertTrue(html.startswith('<html'))
        self.assertIn('FORD3', self.driver.title)
        # They are greeted with their username
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('Welcome, ', header_text)

        # They add their image
        # Chose their provider type

        # They are asked for their tel no.
        inputbox = self.driver.find_element_by_name('telephone')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Primary contact number'
        )

        # Which they enter as
        inputbox.send_keys('0821233444')

        # They are asked for their admission contact no.
        inputbox = self.driver.find_element_by_name('admissions_contact_no')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Admissions contact number'
        )

        # Which they enter as
        inputbox.send_keys('0137441422')

        inputbox = self.driver.find_element_by_name('physical_address_line_1')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Address Line 1'
        )

        inputbox.send_keys('SomeStreet 28')

        inputbox = self.driver.find_element_by_name('physical_address_line_2')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Address Line 2'
        )

        # Which they enter as
        inputbox.send_keys('Extension 9')

        # They are asked for their city.
        inputbox = self.driver.find_element_by_name('physical_address_city')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'City'
        )

        # Which they enter as
        inputbox.send_keys('Nelspruit')

        inputbox = self.driver.find_element_by_name('postal_address')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Postal/ZIP Code'
        )

        # Which they enter as
        inputbox.send_keys('1200')

        # They are asked for their email.
        inputbox = self.driver.find_element_by_name('email')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'example@example.com'
        )

        # Enter their Email Address
        inputbox.send_keys('provider_test@fakedomain.com')

        # They are asked for a campus name.
        inputbox = self.driver.find_element_by_name('campus_name')

        # Enter their Email Address
        inputbox.send_keys('Somecampus')

        # They submit their data by clicking on the submit button
        submit_button = self.driver.find_element_by_class_name('edu-button')
        submit_button.click()

    def test_show_provider(self):
        provider_form_url = reverse(
            'show-provider',
            args=(str(self.new_provider.id)))
        self.assertEqual(
            provider_form_url,
            f'/ford3/providers/{self.new_provider.id}')

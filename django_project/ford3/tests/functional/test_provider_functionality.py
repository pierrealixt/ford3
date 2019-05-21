import unittest
from ford3.tests.functional.utils import SeleniumTestCase, selenium_flag_ready
from ford3.tests.models.model_factories import ModelFactories
from django.contrib.auth.models import User
from django.urls import reverse


class TestProviderForm(SeleniumTestCase):

    def setUp(self):
        self.new_provider = ModelFactories.get_provider_test_object()
        self.provider_form_url = reverse(
            'show-provider',
            args=[str(self.new_provider.id)])

        # logged in first to access any other urls
        self.user = User.objects.create_user(
            'bobby', 'bobby@kartoza.com', 'bob')
        self.client.login(username="bobby", password="bob")
        # logged in, set session so the browser knows it has logged in
        cookie = self.client.cookies['sessionid']
        # selenium will set cookie domain based on current page domain
        self.driver.get(self.live_server_url + '/admin/')
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': cookie.value,
            'secure': False,
            'path': '/'})
        # need to update page for logged in user
        self.driver.refresh()
        self.driver.get(self.live_server_url + '/admin/')

    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def test_provider_form(self):

        # User has created a basic account and now needs to add
        # provider form details and have been redirected to the provider form.
        provider_form_url = reverse(
            'edit-provider',
            args=[str(self.new_provider.id)])

        self.driver.get(f'{self.live_server_url}{provider_form_url}')
        html = self.driver.page_source
        self.assertTrue(html.startswith('<html'))
        self.assertIn('Edit provider', self.driver.title)
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

        inputbox = self.driver.find_element_by_name(
            'physical_address_postal_code')
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

    def test_show_new_provider(self):
        """ It should redirect to the edit form if it's a new provider.
        """
        self.driver.get(f'{self.live_server_url}{self.provider_form_url}')
        self.assertTrue('edit' in self.driver.current_url)

    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def test_return_302(self):
        """ Redirect to login page, even if provider_id or campus_id does not exist.
        """
        # make sure a user has logged out
        self.client.logout()
        # then trying to access the provider
        self.assertTemplateUsed(
            self.driver.get(
                f'{self.live_server_url}{self.provider_form_url}'),
            'login.html')

# coding utf-8
import unittest

from ford3.tests.functional.utils import SeleniumTestCase, selenium_flag_ready



class TestProviderForm(SeleniumTestCase):

    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def test_provider_form(self):

        # User has created a basic account and now needs to add
        # provider form details and have been redirected to the provider form.
        provider_form_url = self.live_server_url + '/ProviderForm/#'
        self.driver.get(provider_form_url)
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

        # They are asked for their admission no.
        inputbox = self.driver.find_element_by_name('admissions_contact_no')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Admissions contact number'
        )

        # Which they enter as
        inputbox.send_keys('0137441422')

        # They are asked for their admission no.
        inputbox = self.driver.find_element_by_name('physical_address_line_1')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Address Line 1'
        )

        # Which they enter as
        inputbox.send_keys('SomeStreet 28')

        # They are asked for their admission no.
        inputbox = self.driver.find_element_by_name('physical_address_line_2')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Address Line 2'
        )

        # Which they enter as
        inputbox.send_keys('Extension 9')

        # They are asked for their admission no.
        inputbox = self.driver.find_element_by_name('physical_address_city')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'City'
        )

        # Which they enter as
        inputbox.send_keys('Nelspruit')

        # They are asked for their admission no.
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




        # They submit their data by clicking on the submit button
        submit_button = self.driver.find_element_by_class_name('edu-button')
        submit_button.click()

        # Since they entered too many digits the form returns an error message

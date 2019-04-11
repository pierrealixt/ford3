import unittest
from ford3.tests.functional.utils import SeleniumTestCase, selenium_flag_ready
from django.urls import reverse
from ford3.tests.models.model_factories import ModelFactories
from selenium.webdriver.common.by import By
from ford3.models import Campus, CampusEvent


class TestCampusForm(SeleniumTestCase):
    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def test_return_404(self):
        """ If provider_id or campus_id does not exist, it should return 404.
        """

        provider_id = '1042'
        campus_id = '2042'

        campus_form_url = reverse('show-campus', args=(provider_id, campus_id))

        self.driver.get(f'{self.live_server_url}{campus_form_url}')
        html = self.driver.page_source

        self.assertIn('404', html)


class TestCampusFormDataBinding(SeleniumTestCase):
    def setUp(self):
        self.provider = ModelFactories.get_provider_test_object(
            new_id=42)
        self.campus = ModelFactories.get_campus_test_object(
            new_id=420)

        campus_form_url = reverse(
            'edit-campus', args=(
                self.provider.id,
                self.campus.id))

        self.campus_form_url = f'{self.live_server_url}{campus_form_url}'

    def test_form_details(self):
        """The form 'Step 1 - Details' should be populated with the correct values.
        """
        form = ['telephone', 'email', 'max_students_per_year']

        self.driver.get(self.campus_form_url)

        for field in form:
            elem = self.driver.find_element_by_id(f'id_campus-details-{field}')
            value = elem.get_attribute('value')
            self.assertEqual(value, getattr(self.campus, field))

    def test_form_location(self):
        """The form 'Step 2 - Location' should be populated with the correct values.
        """
        form = [
            'physical_address_street_name',
            'physical_address_city',
            'physical_address_postal_code'
        ]

        self.driver.get(self.campus_form_url)

        # go to step 2
        next_step_button = self.driver.find_element_by_id('my-next-button')
        next_step_button.click()

        for field in form:
            elem = self.driver.find_element_by_id(
                f'id_campus-location-{field}')
            value = elem.get_attribute('value')
            self.assertEqual(value, getattr(self.campus, field))

    def test_form_events(self):
        """ It should show already created campus's events.
        """

        # go to step 3
        self.driver.get(self.campus_form_url)
        next_step_button = self.driver.find_element_by_id('my-next-button')
        next_step_button.click()
        next_step_button = self.driver.find_element_by_id('my-next-button')
        next_step_button.click()

        pass

    def test_form_qualifications(self):
        """ It should list already selected qualifications.
        """
        saqa = ModelFactories.get_saqa_qualification_test_object()
        form_data = {
            'saqa_ids': f'{saqa.saqa_id}'
        }
        self.campus.save_qualifications(form_data)

        # go to step 4
        self.driver.get(self.campus_form_url)
        next_step_button = self.driver.find_element_by_id('my-next-button')
        next_step_button.click()
        next_step_button = self.driver.find_element_by_id('my-next-button')
        next_step_button.click()
        next_step_button = self.driver.find_element_by_id('my-next-button')
        next_step_button.click()

        qualif_list_ul = self.driver.find_element_by_id(
            'campus-qualifications-list')
        qualif_li = qualif_list_ul.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(qualif_li), 1)

        saqa_ids_elem = self.driver.find_element_by_id(
            'id_campus-qualifications-saqa_ids')
        saqa_ids_value = saqa_ids_elem.get_attribute('value')
        self.assertEqual(saqa_ids_value, str(saqa.saqa_id))

    @unittest.skip('Skip for travis')
    def test_campus_page_add_events(self):
        self.driver.get(self.campus_form_url)
        # User sees the first page's title
        title = self.driver.find_element_by_tag_name('h2').text
        print(title)
        self.assertIn('Campus Details', title)
        # and the footer shows him what page he is on
        self.assert_footer('Page 1 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 2nd page from the footer
        self.assert_footer('Page 2 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 3rd page from the footer
        self.assert_footer('Page 3 of')
        # User sees the 4 form fields - 1 of each and there are 2 hidden inputs
        form_content = self.driver.find_element_by_css_selector(
            '.form-group')
        # Get inputs
        form_inputs = form_content.find_elements_by_tag_name('input')
        self.assertEqual(len(form_inputs), 6)  # 4 form fields + 2 hidden
        self.driver.find_element_by_id(
            'add-campus-event').click()
        form_inputs = form_content.find_elements_by_tag_name('input')
        self.assertEqual(len(form_inputs), 10)  # The existing 6 + 4 new
        # There should now be 2 of each input
        name_inputs = form_content.find_elements_by_name(
            'campus-dates-event_name')
        self.assertEqual(len(name_inputs), 2)
        date_start_inputs = form_content.find_elements_by_name(
            'campus-dates-date_start')
        self.assertEqual(len(date_start_inputs), 2)
        date_end_inputs = form_content.find_elements_by_name(
            'campus-dates-date_end')
        self.assertEqual(len(date_end_inputs), 2)
        http_link_inputs = form_content.find_elements_by_name(
            'campus-dates-http_link')
        self.assertEqual(len(http_link_inputs), 2)
        # The user fills in the data for each field
        name1 = 'Sel Test Name 1'
        name2 = 'Sel Test Name 2'
        name_inputs[0].send_keys(name1)
        date_start_inputs[0].send_keys('04/09/2019')
        date_end_inputs[0].send_keys('05/09/2019')
        http_link_inputs[0].send_keys('www.somelink@testworld.com')
        name_inputs[1].send_keys(name2)
        date_start_inputs[1].send_keys('07/11/2019')
        date_end_inputs[1].send_keys('09/11/2019')
        http_link_inputs[1].send_keys('www.someotherlink@testworld.com')
        # They click next
        self.get_next_button().click()
        # The click submit
        self.get_next_button().click()
        # And 2 campus_events should now be saved by those names
        first_object = list(CampusEvent.objects.filter(name=name1))
        self.assertEqual(len(first_object), 1)
        second_object = list(CampusEvent.objects.filter(name=name2))
        self.assertEqual(len(second_object), 1)

    @unittest.skip('Skip for travis')
    def test_campus_page_add_events_empty_date(self):
        campus_object = Campus.objects.all().first()
        if len(str(campus_object)) > 0:
            pass
        else:
            campus_object = ModelFactories.get_campus_test_object()
        self.driver.get(self.campus_form_url)

        # User sees the first page's title
        title = self.driver.find_element_by_tag_name('h2').text
        print(title)
        self.assertIn('Campus Details', title)
        # and the footer shows him what page he is on
        self.assert_footer('Page 1 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 2nd page from the footer
        self.assert_footer('Page 2 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 3rd page from the footer
        self.assert_footer('Page 3 of')
        # User sees the 4 form fields - 1 of each and there are 2 hidden inputs
        form_content = self.driver.find_element_by_css_selector(
            '.form-group')
        # Get inputs
        form_inputs = form_content.find_elements_by_tag_name('input')
        self.assertEqual(len(form_inputs), 6)  # 4 form fields + 2 hidden
        self.driver.find_element_by_id(
            'add-campus-event').click()
        form_inputs = form_content.find_elements_by_tag_name('input')
        self.assertEqual(len(form_inputs), 10)  # The existing 6 + 4 new
        # There should now be 2 of each input
        name_inputs = form_content.find_elements_by_name(
            'campus-dates-event_name')
        self.assertEqual(len(name_inputs), 2)
        date_start_inputs = form_content.find_elements_by_name(
            'campus-dates-date_start')
        self.assertEqual(len(date_start_inputs), 2)
        date_end_inputs = form_content.find_elements_by_name(
            'campus-dates-date_end')
        self.assertEqual(len(date_end_inputs), 2)
        http_link_inputs = form_content.find_elements_by_name(
            'campus-dates-http_link')
        self.assertEqual(len(http_link_inputs), 2)
        # The user fills in the data for each field
        name1 = 'Sel Test Name 1'
        name2 = 'Sel Test Name 2'
        name_inputs[0].send_keys(name1)
        date_start_inputs[0].send_keys('04/09/2019')
        date_end_inputs[0].send_keys('05/09/2019')
        http_link_inputs[0].send_keys('www.somelink@testworld.com')
        name_inputs[1].send_keys(name2)
        date_start_inputs[1].send_keys('07/11/2119')
        date_end_inputs[1].send_keys('')
        http_link_inputs[1].send_keys('www.someotherlink@testworld.com')
        # They click next
        self.get_next_button().click()
        # The form responds with a validation error
        self.assertIn(self.driver.title, 'FORD3')
        validation_message = self.driver.find_elements_by_name(
            'campus-dates-date_end')[1].get_attribute('validationMessage')
        self.assertEqual(validation_message, 'Please fill out this field.')


    def get_next_button(self):
        next_button = self.driver.find_element_by_id('my-next-button')
        return next_button

    def assert_footer(self, expected_content):
        footer = (
            self.driver.find_element_by_class_name('form-steps-count').text)
        self.assertIn(expected_content, footer)

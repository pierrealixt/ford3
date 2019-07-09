import unittest
from ford3.tests.functional.utils import SeleniumTestCase, selenium_flag_ready
from django.urls import reverse
from ford3.tests.models.model_factories import ModelFactories
from selenium.webdriver.common.by import By
from ford3.models import Campus, CampusEvent, User


class TestCampus(SeleniumTestCase):
    fixtures = ['sa_provinces', 'groups']

    def setUp(self):
        self.campus = ModelFactories.get_campus_test_object()

        provider_url = reverse(
            'show-provider',
            args=[str(self.campus.provider.id)])

        self.driver.get(f'{self.live_server_url}{provider_url}')

    @unittest.skip('Skip for travis')
    def test_create_campus(self):
        new_campus_name = 'New campus name'

        self.assertNotIn(new_campus_name, self.driver.page_source)

        show_modal_button = self.driver.find_element_by_id(
            'open-add-campus-modal')
        show_modal_button.click()

        form = self.driver.find_element_by_id('form-add-campus')
        campus_input = form.find_element_by_css_selector(
            'input[type="text"]')
        campus_input.send_keys(new_campus_name)

        submit = form.find_element_by_tag_name('button')
        submit.click()

        self.assertIn(new_campus_name, self.driver.page_source)

    @unittest.skip('Skip for travis')
    def test_create_duplicate_campus(self):
        new_campus_name = self.campus.name

        show_modal_button = self.driver.find_element_by_id(
            'open-add-campus-modal')
        show_modal_button.click()

        form = self.driver.find_element_by_id('form-add-campus')

        campus_input = form.find_element_by_css_selector('input[type="text"]')
        campus_input.send_keys(new_campus_name)

        submit = form.find_element_by_tag_name('button')
        submit.click()

        self.assertIn(new_campus_name, self.driver.page_source)

        form = self.driver.find_element_by_id('form-add-campus')
        error = form.find_element_by_id('campus-error')

        self.assertEqual(
            error.get_attribute('innerHTML'),
            'Name is already taken.')


class TestCampusForm(SeleniumTestCase):
    fixtures = [
        'groups',
        'sa_provinces',
        'test_province_users',
        'test_provider_users',
        'test_campus_users',
        'test_providers'
    ]

    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def setUp(self):
        self.campus_form_url = reverse('show-campus', args=('1042', '2042'))

        # logged in first to access any other urls
        self.user = User.objects.get(pk=1)
        # .create_user(
        #     'bobby', 'bobby@kartoza.com', 'bob')
        self.client.force_login(self.user, backend=None)
        # self.client.login(username="bobby", password="bob")
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
    def test_return_404(self):
        """ If provider_id or campus_id does not exist, it should return 404.
        """
        self.driver.get(f'{self.live_server_url}{self.campus_form_url}')
        html = self.driver.page_source

        self.assertIn('404', html)

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
            self.driver.get(f'{self.live_server_url}{self.campus_form_url}'),
            'login.html')


class TestCampusFormDataBinding(SeleniumTestCase):
    fixtures = ['sa_provinces']

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
        # logged in first to access any other urls
        self.user = User.objects.create_user(
            'bobby2', 'bobby2@kartoza.com', 'bob')
        self.client.login(username="bobby2", password="bob")
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
            'physical_address_line_1',
            'physical_address_line_2',
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
            'saqa_ids': f'{saqa.id}'
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
        qualif_li = qualif_list_ul.find_elements(By.CLASS_NAME, 'qualif-li')
        self.assertEqual(len(qualif_li), 1)

        saqa_ids_elem = self.driver.find_element_by_id(
            'id_campus-qualifications-saqa_ids')
        saqa_ids_value = saqa_ids_elem.get_attribute('value')
        self.assertEqual(saqa_ids_value, str(saqa.id))

    @unittest.skip('Skip for travis')
    def test_campus_page_add_events(self):
        self.driver.get(self.campus_form_url)
        # User sees the first page's title
        title = self.driver.find_element_by_tag_name('h2').text

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

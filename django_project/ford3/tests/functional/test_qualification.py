import unittest
from ford3.tests.functional.utils import SeleniumTestCase, selenium_flag_ready
from django.urls import reverse
from ford3.tests.models.model_factories import ModelFactories
from ford3.models import QualificationEvent, User


class TestQualificationForm(SeleniumTestCase):
    fixtures = ['sa_provinces', 'groups']

    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def setUp(self):
        # url of non-existed campus
        self.campus_form_url = reverse('show-campus', args=('1042', '2042'))
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


class TestQualificationFormDataBinding(SeleniumTestCase):
    def setUp(self):
        self.provider = ModelFactories.get_provider_test_object(
            new_id=42)
        self.campus = ModelFactories.get_campus_test_object(
            new_id=420)
        self.qualification = ModelFactories.get_qualification_test_object()
        self.qualification.campus = self.campus
        qualification_form_url = reverse(
            'edit-qualification', args=(
                self.provider.id,
                self.campus.id,
                self.qualification.id))

        self.qualification_form_url = (
            f'{self.live_server_url}{qualification_form_url}')

    @unittest.skip("Skip for travis")
    def test_qualification_add_events(self):
        self.driver.get(self.qualification_form_url)
        # User sees the first page's title
        title = self.driver.find_element_by_tag_name('h3').text
        self.assertEqual(title, 'SAQAQualification name')
        # and the footer shows him what page he is on
        self.assert_footer('Step 1 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 2nd page from the footer
        self.assert_footer('Step 2 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 3rd page from the footer
        self.assert_footer('Step 3 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 3rd page from the footer
        self.assert_footer('Step 4 of')
        # User clicks next
        self.get_next_button().click()
        # User sees they are on the 3rd page from the footer
        self.assert_footer('Step 5 of')
        # User sees the 4 form fields - 1 of each and there are 2 hidden inputs
        form_content = self.driver.find_element_by_css_selector(
            '.form-group')
        # Get inputs
        form_inputs = form_content.find_elements_by_tag_name('input')
        self.assertEqual(len(form_inputs), 6)  # 4 form fields + 2 hidden
        self.driver.find_element_by_id(
            'add-qualification-event').click()
        form_inputs = form_content.find_elements_by_tag_name('input')
        self.assertEqual(len(form_inputs), 10)  # The existing 6 + 4 new
        # There should now be 2 of each input
        name_inputs = form_content.find_elements_by_name(
            '4-name')
        self.assertEqual(len(name_inputs), 2)
        date_start_inputs = form_content.find_elements_by_name(
            '4-date_start')
        self.assertEqual(len(date_start_inputs), 2)
        date_end_inputs = form_content.find_elements_by_name(
            '4-date_end')
        self.assertEqual(len(date_end_inputs), 2)
        http_link_inputs = form_content.find_elements_by_name(
            '4-http_link')
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
        # The click submit
        self.get_next_button().click()
        # And 2 qualification_events should now be saved by those names
        first_object = list(QualificationEvent.objects.filter(name=name1))
        self.assertEqual(len(first_object), 1)
        second_object = list(QualificationEvent.objects.filter(name=name2))
        self.assertEqual(len(second_object), 1)

    def get_next_button(self):
        next_button = self.driver.find_element_by_id('my-next-button')
        return next_button

    def assert_footer(self, expected_content):
        footer = (
            self.driver.find_element_by_class_name('form-steps-count').text)
        self.assertIn(expected_content, footer)

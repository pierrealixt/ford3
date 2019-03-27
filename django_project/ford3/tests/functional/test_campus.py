import unittest
from ford3.tests.functional.utils import SeleniumTestCase, selenium_flag_ready
# from ford3.tests.models.model_factories import ModelFactories
# from selenium.webdriver.common.by import By


def build_campus_form_url(base_url, provider_id, campus_id):
    return '/'.join([
        base_url,
        'providers/{}'.format(provider_id),
        'campus/{}'.format(campus_id),
        'edit'
    ])


class TestCampusForm(SeleniumTestCase):
    @unittest.skipUnless(
        selenium_flag_ready(),
        'Selenium test was not setup')
    def test_return_404(self):

        """
        If provider_id or campus_id does not exist
        It should return 404
        """

        provider_id = 1042
        campus_id = 2042

        campus_form_url = build_campus_form_url(
            self.live_server_url,
            provider_id,
            campus_id)

        self.driver.get(campus_form_url)
        html = self.driver.page_source

        self.assertIn('404', html)

    # def test_show_wizard(self):
    #     pass
    #     provider = ModelFactories.get_provider_test_object(
    #         new_id=42)
    #     campus = ModelFactories.get_campus_test_object(
    #         new_id=420)

    #     campus_form_url = build_campus_form_url(
    #         self.live_server_url,
    #         provider.id,
    #         campus.id)

    #     self.driver.get(campus_form_url)
    #     html = self.driver.page_source

    #     self.assertIn('Object Test Name Campus Details', html)

    #     # Step 1 - Details

    #     self.assertIn('Tel. Number', html)
    #     self.assertIn('Email', html)
    #     self.assertIn('Maximum number of Students per year in campus', html)

    #     next_step_button = self.driver.find_elements(By.LINK_TEXT, 'Next')
    #     next_step_button.click()

    #     html = self.driver.page_source

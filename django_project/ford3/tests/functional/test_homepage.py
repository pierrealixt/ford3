from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestHomepage(TestCase):

    def setUp(self):
        self.browser = webdriver.Remote("http://172.29.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://172.20.10.13')
        self.assertIn('FORD3', self.browser.title)


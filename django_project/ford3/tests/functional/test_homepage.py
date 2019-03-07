# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # noqa
#
#
# class TestHomepage(TestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Remote("http://172.21.0.1:4444/wd/hub",
#                                   DesiredCapabilities.CHROME)
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def runTest(self):
#         self.browser.get('http://10.0.0.6:80')
#         self.assertIn('FORD3', self.browser.title)

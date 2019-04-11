# coding=utf-8
import logging

from contextlib import contextmanager
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

LOGGER = logging.getLogger(__file__)


def selenium_flag_ready():
    """Flag to tell that selenium test is setup."""
    return settings.SELENIUM_DRIVER and settings.SELENIUM_UNIT_TEST_FLAG


class SeleniumTestCase(StaticLiveServerTestCase):

    host = settings.SELENIUM_TEST_HOSTNAME
    port = settings.SELENIUM_TEST_PORT
    implicit_wait = 60
    desired_capabilities = DesiredCapabilities.FIREFOX
    command_executor = settings.SELENIUM_DRIVER

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()
        # Create a new instance of the driver
        cls.driver = None
        if selenium_flag_ready():
            cls.driver = webdriver.Remote(
                command_executor=cls.command_executor,
                desired_capabilities=cls.desired_capabilities)
            cls.driver.implicitly_wait(cls.implicit_wait)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    @contextmanager
    def disable_implicit_wait(self):
        """Disable the default implicit wait."""
        self.selenium.implicitly_wait(0)
        try:
            yield
        finally:
            self.selenium.implicitly_wait(self.implicit_wait)

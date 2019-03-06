# SELENIUM

---

## Use selenium-docker from another docker

1. get host machine IP from docker container (make shell)

    /sbin/ip route|awk '/default/ { print $3 }'

2. in the same docker container, start a local server

    ./manage runserver 0.0.0.0:8080

3. get local host ip (Network settings)

4. run selenium in a docker container

    docker run -d -p 4444:4444 selenium/standalone-chrome
    
    docker run -d -p 4444:4444 selenium/standalone-firefox

5. easy selenium test

    from django.test import TestCase
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    
    
    class TestHomepage(TestCase):
    
        def setUp(self):
            driver = webdriver.Remote("http://HOST_IP_FROM_DOCKER:4444/wd/hub", DesiredCapabilities.CHROME)
    
            def tearDown(self):
            self.browser.quit()
    
        def runTest(self):
            self.browser.get('http://LOCAL_HOST_IP')
            self.assertIn('Penbra', self.browser.title)

6. run the test from the HOST machine

    make test
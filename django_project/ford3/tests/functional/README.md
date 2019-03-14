# SELENIUM IN DOCKER

This guide is intended as a generic README to be copy-pasted between project.

Authors:
 - Pierre-Alix <pierrealix@kartoza.com>
 - Rizky Maulana Nugraha <rizky@kartoza.com, lana.pcfre@gmail.com>

---

## Use selenium-docker in this orchestration (ansible setup)

1. Selenium docker-compose file is already integrated in the Makefile.

   To start up selenium:
   
   `make selenium-up`
   
   To shutdown selenium:
   
   `make selenium-down`
   
   To restart (from already started up selenium), just chain the command together:
   
   `make selenium-down selenium-up`
   
2. Creating a selenium unit test

   Some general rule of advice:
   As a helper, extends your unit test from our custom SeleniumTestCase, which covers 
   some basic cleanup functions and checks for Selenium in Docker.
   Decorate your test function to check that Selenium Test connection 
   is properly configured.
   For a functional testing, any configuration error should fail immediately.
   Meanwhile, runtime error should be handled according to what your functional 
   test were intended to do. Is it expected to fail the test (asserted) or not.
   SeleniumTestCase extends from LiveServerTestCase. It will contain member functions
   and attributes of that class, such as `self.live_server_url` or `self.port`.
   
   The snippet below shows a sample of unit test.
   
   
	class TestHomepage(SeleniumTestCase):
	
        @unittest.skipUnless(
            selenium_flag_ready(),
            'Selenium Test was not set up')
        def test_title(self):
            # test that driver perfectly configured
            self.assertTrue(self.driver)
        	
            # connect to server
            self.driver.get(self.live_server_url)
			
            # test things...
            self.assertIn('the title', self.driver.title)

3. Viewing selenium test while it is running

   We are using selenium grid as the driver, then change the container (the browser) 
   that the test runs. By default we are using `firefox-debug` image.
   To view what happens, connect using a VNC viewer with the following credentials:
   
   - host: localhost or your ip address or domain alias
   - port: 5900 (default port in selenium-compose)
   - password: secret (default password)
   
4. Running the test

   Run the test using django manage.py test, as per default django workflow.
   
   `python manage.py test --noinput <test package>`
   
   Or if you want to run the test in bulk. Just run it from make command.
   
   `make test`

## Use selenium-docker from another separate docker containers

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

## General FAQ

If you encounter new problem/solution. Please add the entry.

1. My test does not run at all.

   You need to have any selenium driver up and running.
   If you use docker driver like in this orchestration, use `make status` or 
   other docker commands to see if you have your selenium grid/hub and runner.
   
2. My test says that address is in use.

   In this orchestration we bind the django live test server to the same
   port that we use for `python manage.py runserver` command. This is so we 
   are able to see the server from local browser if we wish to do that. 
   If you run selenium test, shutdown your development server.
   If you want to start development server, make sure you don't run selenium test.
   
3. I did no 2, and my test runs fine. But when I run it again, it says address in use.

   The previous test doesn't quit the driver properly. Generally we try to quit
   the driver after *the test class* finished. Just try again after a couple of minutes.
   If this persists, restart your selenium driver.
   
4. I want to run the manage.py server with different port than the test server.

   Maybe you don't want to use the same port. 
   Probably you want to see the test just via VNC.
   Set your `SELENIUM_TEST_PORT` environment variable in `all.yml` or 
   `docker-compose.override.yml` (temporary) in your django service to `0`
   
   This means Django LiveServerTestCase will use random available port.
   If you want a fixed port, just put any available port there, like `8081`

5. I want to run selenium test in the `real grid` somewhere over the internet.

   Put your driver command URL in `SELENIUM_DRIVER` environment variable
   
6. My selenium test have weird layout.

   You forgot to run `make collectstatic`.
   We can actually uses `StaticLiveServerTestCase` as a base (no need to run collectstatic), 
   but since this is intended as a functional test case,
   It's best to also check that your static files are collected properly.
   
7. I want to use a certain data available in the test server.

   You want this: https://docs.djangoproject.com/en/2.1/topics/testing/tools/#fixture-loading
   Yeah, the test case extends from LiveServerTestCase, so you can do that too.

8. The javascript/css library in CDN does not work.

   Your selenium driver container needs to be able to access internet.
   Something is wrong with your Docker app or DNS resolver.
   
9. Selenium driver can't connect to Django test server.

   Check your `SELENIUM_TEST_HOSTNAME` and `SELENIUM_TEST_PORT` environment variable 
   in `all.yml` and `docker-compose.override.yml` file. Make sure it can reach 
   the container where you run `manage.py test`. You have to use docker-common sense 
   here. Go inside your driver container, then curl/ping/wget to your django container.
   
   For example, if your django service is called `uwsgi`. You should be able to
   `ping uwsgi` or `wget uwsgi` when the server is running. Or at least it will 
   get the correct ipaddress.
   
   If you use separate selenium stack (different stack from the main project), 
   then you have set `SELENIUM_TEST_HOSTNAME` to the correct resolvable ipaddress/domain name,
   accessible from that driver. Make sure the `SELENIUM_TEST_PORT` that is being used is open too.

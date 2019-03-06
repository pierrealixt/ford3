# import unittest
from django.test import TestCase
import os
import sys
from subprocess import Popen, PIPE


__copyright__ = "Copyright 2016, The InaSAFE Project"
__license__ = "GPL version 3"
__email__ = "info@inasafe.org"
__revision__ = '$Format:%H$'


class TestPythonStyle(TestCase):


    def test_flake8(self):
        """Test if the code is Flake8 compliant."""
        command = ['flake8']
        root = './'
        output = Popen(command, stdout=PIPE, cwd=root).communicate()[0]
        default_number_lines = 0

        # if os.environ.get('ON_TRAVIS', False):
        #     root = '../'
        #     command = ['flake8']
        #     output = Popen(command, stdout=PIPE, cwd=root).communicate()[0]
        #     default_number_lines = 0
        # elif sys.platform.startswith('win'):
        #     # ET I don't know on windows.
        #     pass

        # else:
        #     # OSX and linux just delegate to make
        #     root = '../../'
        #     command = ['make', 'flake8']
        #     output = Popen(command, stdout=PIPE, cwd=root).communicate()[0]
        #     default_number_lines = 0


        lines = len(output.splitlines()) - default_number_lines
        print (output)
        message = (
            'Hey mate, go back to your keyboard :) (expected %s, got %s '
            'lines from PEP8.)' % (default_number_lines, lines))
        self.assertEquals(lines, 0, message)

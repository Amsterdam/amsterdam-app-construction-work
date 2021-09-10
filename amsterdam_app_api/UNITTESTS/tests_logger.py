import os
import logging
from unittest.mock import patch, call
from django.test import TestCase
from amsterdam_app_api.GenericFunctions.Logger import Logger


class TestLogger(TestCase):
    def test_logger_debug_enabled(self):
        debug = os.environ.get('DEBUG', '')
        os.environ['DEBUG'] = 'true'
        logger = Logger()

        with patch('builtins.print') as mocked_print:
            logger.info('info')
            assert mocked_print.call_args_list == [call('info')]

        with patch('builtins.print') as mocked_print:
            logger.debug('debug')
            assert mocked_print.call_args_list == [call('debug')]

        with patch('builtins.print') as mocked_print:
            logger.error('error')
            assert mocked_print.call_args_list == [call('error')]

        os.environ['DEBUG'] = debug

    def test_logger_debug_disabled(self):
        debug = os.environ.get('DEBUG', '')
        os.environ['DEBUG'] = 'false'

        logger = Logger()
        mock_logging = logging.getLogger('amsterdam_app_api.GenericFunctions.Logger')
        with patch.object(mock_logging, 'info') as mocked_log:
            logger.info('info')
            assert mocked_log.call_args_list == [call('info')]

        with patch.object(mock_logging, 'debug') as mocked_log:
            logger.debug('debug')
            assert mocked_log.call_args_list == [call('debug')]

        with patch.object(mock_logging, 'error') as mocked_log:
            logger.error('error')
            assert mocked_log.call_args_list == [call('error')]

        os.environ['DEBUG'] = debug

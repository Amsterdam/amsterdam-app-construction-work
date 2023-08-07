""" unit_tests """

import logging
import os
from unittest.mock import call, patch

from django.test import TestCase

from construction_work.generic_functions.generic_logger import Logger


class TestLogger(TestCase):
    """Test logging facility"""

    def test_logger_debug_enabled(self):
        """test logger debug level"""
        debug = os.environ.get("DEBUG", "")
        os.environ["DEBUG"] = "true"
        logger = Logger()

        with patch("builtins.print") as mocked_print:
            logger.info("info")
            assert mocked_print.call_args_list == [call("info")]

        with patch("builtins.print") as mocked_print:
            logger.debug("debug")
            assert mocked_print.call_args_list == [call("debug")]

        with patch("builtins.print") as mocked_print:
            logger.error("error")
            assert mocked_print.call_args_list == [call("error")]

        os.environ["DEBUG"] = debug

    def test_logger_debug_disabled(self):
        """test logger debug disabled"""
        debug = os.environ.get("DEBUG", "")
        os.environ["DEBUG"] = "false"

        logger = Logger()
        mock_logging = logging.getLogger("construction_work.generic_functions.generic_logger")
        with patch.object(mock_logging, "info") as mocked_log:
            logger.info("info")
            assert mocked_log.call_args_list == [call("info")]

        with patch.object(mock_logging, "debug") as mocked_log:
            logger.debug("debug")
            assert mocked_log.call_args_list == [call("debug")]

        with patch.object(mock_logging, "error") as mocked_log:
            logger.error("error")
            assert mocked_log.call_args_list == [call("error")]

        os.environ["DEBUG"] = debug

import logging

import loguru


class LoguruInterceptHandler(logging.Handler):
    """This handler intercepts standard logging messages and redirects them to loguru.

    It is used in order to allow hooking in to logging messages emmitted by fastflow's
    dependencies.

    For more information:

    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging

    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level, if it exists
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

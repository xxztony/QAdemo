import inspect
import logging
import os
import sys

from colorama import Fore, Style, init

IS_LOGGER_SETUP = False
# the init call
init()
LEVEL_COLORS = {
    'DEBUG': Fore.CYAN,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.RED + Style.BRIGHT,
}


class ColoredFormatter(logging.Formatter):
    """

    """

    def __init__(self, *args, **kwargs):
        self.use_color = kwargs.pop('use_color', True)
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        """

        :param record:
        :return:
        """
        levelname = record.levelname
        if not hasattr(record, 'use_color'):
            record.use_color = True
        if self.use_color and record.use_color:
            if not hasattr(record, 'level_color'):
                record.level_color = LEVEL_COLORS[levelname]
            if not hasattr(record, 'color'):
                record.color = LEVEL_COLORS[levelname]
            record.cyan = Fore.CYAN
            record.green = Fore.GREEN
            record.yellow = Fore.YELLOW
            record.red = Fore.RED
            record.blue = Fore.BLUE
            record.magenta = Fore.MAGENTA
        else:
            record.level_color = ''
            record.color = ''
            record.cyan = ''
            record.green = ''
            record.yellow = ''
            record.red = ''
            record.blue = ''
            record.magenta = ''
        msg = super().format(record)
        if self.use_color and record.use_color:
            return f"{msg}{Style.RESET_ALL}"
        return msg


def setup_logger(name=None, format=None, level=None, use_color=True):
    """
    setup logger
    :param name:
    :param format: log format
    :param level: log level
    :param use_color: log color
    :return: logger
    """
    global IS_LOGGER_SETUP
    if not IS_LOGGER_SETUP:
        if level is None:
            level = logging.INFO
        # You can turn on debug with --debug=1 in args, or environment variable IS_DEBUG_ENV=1
        debug_env = os.getenv('IS_DEBUG_ENV', '0').lower()
        for arg in sys.argv:
            if ('debug=1' in arg.lower()
                    or debug_env == 'true' or debug_env == '1'):
                level = logging.DEBUG
                break

        handler = logging.StreamHandler()
        handler.setLevel(level)
        logging_format = "%(color)s[%(asctime)s.%(msecs)03d][%(name)s], [%(levelname)s]: %(message)s -<module:%(module)s,line:%(lineno)d >" if not format else format
        formatter = ColoredFormatter(
            fmt=logging_format,
            datefmt='%H:%M:%S',
            use_color=use_color
        )
        handler.setFormatter(formatter)
        # root logger
        name = '' if not name else name
        logger = logging.getLogger(name)
        logger.setLevel(level)
        # avoid duplicate logging message
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)

        IS_LOGGER_SETUP = True
    return logger


class CustomLogger:
    """
    This class is the log class for print test logs
    """
    logger = setup_logger()

    @staticmethod
    def print_step(msg, use_color=True, color=None):
        CustomLogger.logger.info("Step: " + msg, extra={'use_color': use_color,
                                                        'color': Fore.GREEN if not color else color})

    @staticmethod
    def print_with_new_line(msg, use_color=True):
        CustomLogger.logger.info('')
        CustomLogger.logger.info(msg, extra={'use_color': use_color})

    @staticmethod
    def print_start(use_color=True):
        CustomLogger.logger.info('')
        CustomLogger.logger.info('TestCase: {}'.format(inspect.stack()[1][3]),
                                 extra={'use_color': use_color, 'color': Fore.BLUE})

    @staticmethod
    def print_global_msg(msg, use_color=True):
        CustomLogger.logger.info('')
        CustomLogger.logger.info(msg, extra={'use_color': use_color, 'color': Fore.BLUE})

    @staticmethod
    def print_log(msg, use_color=True):
        CustomLogger.logger.info(msg, extra={'use_color': use_color, 'color': Fore.MAGENTA})

    @staticmethod
    def print_debug(msg, use_color=True, error=False, quiet=False):
        if not quiet:
            if error:
                CustomLogger.logger.info(msg, extra={'use_color': use_color, 'color': LEVEL_COLORS['DEBUG']})
            else:
                CustomLogger.logger.debug(msg, extra={'use_color': use_color})

    @staticmethod
    def print_error(msg):
        CustomLogger.logger.error(msg)

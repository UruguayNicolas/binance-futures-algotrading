import colorlog
import logging
import warnings

# Remove FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Configure colorlog
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Configure handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Configure loglevel
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

import logging
from rumpy.client import RumClient
from rumpy.client.module import *

__version__ = "0.0.8"
__author__ = "liujuanjuan1984"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())

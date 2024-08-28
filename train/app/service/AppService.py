import logging

from train.app.configuration.LoggingConfig import stream_handler, \
    file_handler
from train.app.entity.App import App

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def is_service_game_code(app : App):
    return app != None

import json
import logging
import os

from google.cloud import pubsub_v1

from train.app.configuration.LoggingConfig import stream_handler, \
    file_handler
from train.app.domain.CrashReportMessage import InitMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)



def publish_message(topic_id: str, message: InitMessage):
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),topic=topic_id)
    logger.debug(f"Publishing message to {topic_name}")
    data = json.dumps(message.log).encode("utf-8")
    publisher.publish(topic_name, data)

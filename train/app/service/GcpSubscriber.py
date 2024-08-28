import logging
import os
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor

from google.cloud import pubsub_v1


from train.app.configuration.LoggingConfig import stream_handler, \
    file_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

timeout = 30.0
# threads will be created.
executor = futures.ThreadPoolExecutor(max_workers=5)
# A thread pool-based scheduler. It must not be shared across SubscriberClients.
scheduler = pubsub_v1.subscriber.scheduler.ThreadScheduler(executor)

def callback(message):
    print(message.data)
    message.ack()

def subscribe():
    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_name = subscriber.subscription_path( os.getenv('GOOGLE_CLOUD_PROJECT'), 'edge.crash.v3.consumer')
        logger.debug(f"Subscribing to {subscription_name}")
        future = subscriber.subscribe(subscription_name, callback=callback, scheduler=scheduler)
        try:
            future.result()
        except TimeoutError:
            future.cancel() # Trigger the shutdown.
            future.result() # Block until the shutdown is complete.
            logger.info("Subscriber stopped. due to TimeoutError")
        except KeyboardInterrupt:
            future.cancel() # Trigger the shutdown.
            future.result() # Block until the shutdown is complete.
            logger.info("Subscriber stopped. due to KeyboardInterrupt")




executor = ThreadPoolExecutor(max_workers=2)
executor.submit(subscribe)
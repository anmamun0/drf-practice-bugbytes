import logging
import time
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def send_email_task():
    logger.info("Sending email...")
    time.sleep(5)
    logger.info("Email sent successfully!")

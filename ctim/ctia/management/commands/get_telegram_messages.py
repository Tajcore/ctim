import logging

from django.core.management.base import BaseCommand

from ctim.ctia.tasks.get_telegram_channelposts import get_telegram_channelposts


class Command(BaseCommand):
    help = "Runs the get_telegram_channelposts Celery task"

    def add_arguments(self, parser):
        # Optional: Add arguments here if you need to customize the task call
        parser.add_argument("channel_name", type=str, help="Channel name to process")
        parser.add_argument(
            "--loglevel",
            type=str,
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            default="INFO",
            help="Logging level to use for the task",
        )

    def handle(self, *args, **options):
        channel_name = options["channel_name"]
        loglevel = options["loglevel"].upper()

        self.stdout.write(f"Log level {loglevel}")

        # Set the logging level
        logger = logging.getLogger("ctim.ctia.tasks.get_telegram_channelposts")
        logger.setLevel(getattr(logging, loglevel))

        self.stdout.write(f"Running task for channel: {channel_name} with log level {loglevel}")

        # Trigger the Celery task
        get_telegram_channelposts.delay(channel_name)

        self.stdout.write(f"Task triggered for channel: {channel_name}")

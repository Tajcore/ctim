import json
import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

from ctim.ctia.models.ransomware import Group, Post


# Configure logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load Ransomware Post data from JSON file into PostgreSQL database"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file",
            type=str,
            nargs="?",  # Makes the argument optional
            default=settings.DEFAULT_RANSOMWARE_POSTS_JSON,
            help="The JSON file to parse or URL to fetch data from",
        )

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]
        try:
            if json_file.startswith("http://") or json_file.startswith("https://"):
                response = requests.get(json_file)
                response.raise_for_status()
                data = response.json()
            else:
                with open(json_file) as file:
                    data = json.load(file)
            for item in data:
                try:
                    group_name = item["group_name"]
                    group, _ = Group.objects.get_or_create(name=group_name)

                    Post.objects.update_or_create(
                        title=item["post_title"],
                        url=item["post_url"],
                        defaults={
                            "group": group,
                            "discovered": self.parse_datetime(item["discovered"]),
                            "description": item.get("description", None),
                            "website": item.get("website", None),
                            "published": self.parse_datetime(item["published"]),
                            "country": item["country"],
                        },
                    )
                except IntegrityError as e:
                    logger.error(f"Error saving post {item['post_title']}: {e}")
        except Exception as e:
            logger.error(f"Error processing file {json_file}: {e}")
            raise e
        else:
            self.stdout.write(self.style.SUCCESS("Successfully parsed JSON file"))

    def parse_datetime(self, dt_str):
        """Convert a date-time string to a timezone-aware datetime object."""
        dt = parse_datetime(dt_str) if dt_str else None
        return make_aware(dt) if dt and not is_aware(dt) else dt

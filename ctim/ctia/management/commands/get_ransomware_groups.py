import json
import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

from ctim.ctia.models.ransomware import Group, Location, Profile

# Configure logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load Ransomware Group data from JSON file into PostgreSQL database"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file",
            type=str,
            nargs="?",  # Makes the argument optional
            default=settings.DEFAULT_RANSOMWARE_GROUPS_JSON,
            help="The JSON file to parse or URL to fetch data from",
        )

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]
        self.stdout.write(f"Running handle for json_file: {json_file}")
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
                    self.stdout.write(f"Running update_or_create for group: {item['name']}")
                    group, created = Group.objects.update_or_create(
                        name=item["name"],
                        defaults={
                            "captcha": item.get("captcha", False),
                            "parser": item.get("parser", False),
                            "javascript_render": item.get("javascript_render", False),
                            "meta": item.get("meta"),
                            "description": item.get("description"),
                        },
                    )
                    self.load_locations(group, item.get("locations", []))
                    self.load_profiles(group, item.get("profile", []))
                except IntegrityError as e:
                    logger.error(f"Error saving group {item['name']}: {e}")
        except Exception as e:
            logger.error(f"Error processing file {json_file}: {e}")
            raise e

    def load_locations(self, group, locations):
        for location in locations:
            try:
                Location.objects.update_or_create(
                    group=group,
                    fqdn=location["fqdn"],
                    defaults={
                        "title": location.get("title", "Default Title"),
                        "version": location["version"],
                        "slug": location["slug"],
                        "available": location["available"],
                        "delay": location.get("delay"),
                        "updated": self.parse_datetime(location.get("updated")),
                        "lastscrape": self.parse_datetime(location.get("lastscrape")),
                        "enabled": location["enabled"],
                    },
                )
            except IntegrityError as e:
                logger.error(f"Error saving location for group {group.name}: {e}")

    def parse_datetime(self, dt_str):
        dt = parse_datetime(dt_str) if dt_str else None
        return make_aware(dt) if dt and not is_aware(dt) else dt

    def load_profiles(self, group, profiles):
        for profile_url in profiles:
            try:
                Profile.objects.update_or_create(group=group, url=profile_url)
            except IntegrityError as e:
                logger.error(f"Error saving profile for group {group.name}: {e}")

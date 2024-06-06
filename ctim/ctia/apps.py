# ctim/ctia/apps.py
from django.apps import AppConfig


class CtiaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ctim.ctia"
    verbose_name = "Cyber Threat Intelligence Agents"

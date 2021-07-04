from allauth.account import app_settings as allauth_settings
from django.conf import settings

TEMPLATE_EXTENSION = getattr(
    settings, "ALLAUTH_2F2A_TEMPLATE_EXTENSION", allauth_settings.TEMPLATE_EXTENSION
)

ALWAYS_REVEAL_BACKUP_TOKENS = bool(
    getattr(settings, "ALLAUTH_2F2A_ALWAYS_REVEAL_BACKUP_TOKENS", True)
)

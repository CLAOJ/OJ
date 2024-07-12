try:
    from turnstile.fields import TurnstileField
except ImportError:
    TurnstileField = None
else:
    from django.conf import settings
    if not (hasattr(settings, 'TURNSTILE_SITEKEY') and hasattr(settings, 'TURNSTILE_SECRET')):
        TurnstileField = None

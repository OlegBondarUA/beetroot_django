from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader


def send_html_email(
        *,
        subject: str,
        template_name: str,
        context: dict[str, Any],
        to_emails: list[str],
        from_email: str | None = settings.DEFAULT_FROM_EMAIL,
        message: str | None = '',
):
    html_message = loader.render_to_string(template_name, context)
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=to_emails,
        html_message=html_message
    )


from django.core.mail import send_mail
from django.conf import settings

def send_email(subject: str, message: str, recipient_list: list, from_email: str = None, fail_silently: bool = False) -> None:
    """
    Sends an email using Django's email backend.

    Args:
        subject (str): Subject of the email.
        message (str): Body of the email.
        recipient_list (list): List of recipient email addresses.
        from_email (str, optional): Sender's email address. Defaults to settings.DEFAULT_FROM_EMAIL.
        fail_silently (bool, optional): Whether to suppress exceptions. Defaults to False.

    Returns:
        None
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
    )


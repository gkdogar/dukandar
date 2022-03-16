from django.template.loader import get_template
from django.core.mail import EmailMessage



def send_password_reset(url, reciever):
    """
        Send email to user with password reset detail.
    """
    ctx = {
        'url': url,
    }
    message = get_template("templated_email/fimbay_reset_email_template.html").render(ctx)
    mail = EmailMessage(
        subject="Password Reset Email",
        body=message,
        from_email='postmaster@fimbay.com',
        to=[reciever],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=False)

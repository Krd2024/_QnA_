from decouple import config
from django.core.mail import EmailMessage

EMAIL = config("EMAIL_HOST_USER")
PWD = config("EMAIL_HOST_PASSWORD")


def send_mail_(subject, to, message):
    email = EmailMessage(
        subject=subject,
        body="1",
        from_email=EMAIL,
        to=[to],
        headers={"Content-Type": 'text/html; charset="utf-8"'},
    )

    # Прикрепите файл к письму
    message.seek(0)
    email.attach("image.jpg", message.read(), message.content_type)

    # Отправьте письмо
    email.send()


print("Email sent with the image attachment.")

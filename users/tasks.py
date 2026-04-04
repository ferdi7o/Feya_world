from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        subject = 'Добре дошли във Feya World!'
        message = f'Здравейте, {user.username}!\n\nБлагодарим ви, че се регистрирахте в нашия магазин. Вашият акаунт е успешно създаден.'
        email_from = 'noreply@feyaworld.com'
        recipient_list = [user.email]

        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        return f"Email sent to {user.email}"
    except Exception as e:
        return str(e)
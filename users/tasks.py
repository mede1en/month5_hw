from email import message

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser
from django.utils import timezone

@shared_task
def add(x,y): #deley
    print(f"----------------->args {x} and {y}---------------------->")
    # from time import sleep
    # sleep(15)
    return x+y

#дз
@shared_task
def send_confirmation_code(user_email: str, code: str):# SMTP
    """Отправляет письмо с кодом подтверждения на email"""
    subject = "Подтверждение регистрации"
    message = f"Ваш код подтверждения: {code}"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["abdillaevamedina6@gmail.com"],
        fail_silently=False,
    )
    return {'email': user_email, 'code': code}


@shared_task
def delete_inactive_users(): # crontab
    """Удаляет неактивные аккаунты старше 1 дня"""
    inactive_users = CustomUser.objects.filter(
        is_active=False,
        date_joined__lt=timezone.now() - timezone.timedelta(days=1),
    )
    deleted_count, _ = inactive_users.delete()
    return {'deleted': deleted_count}

# @shared_task
# def send_otp_mail(email, otp):
#     print("sending" * 10)
#     send_mail(
#         subject="You otp code",
#         message=f"otp code:{otp}",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email],
#         fail_silently=False,
#     )
#     return "OK"
#
#
# @shared_task
# def send_report_mail():
#     print("sending" * 10)
#     send_mail(
#         subject="Report data",
#         message="что то очень важное",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=["abdillaevamedina6@gmail.com"],
#         fail_silently=False,
#     )
#     return "OK"



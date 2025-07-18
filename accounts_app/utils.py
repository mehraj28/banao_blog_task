from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_calendar_instructions(doctor_email, doctor_name):
    subject = 'Google Calendar Integration Instructions'
    message = render_to_string('calendar_instructions_email.html', {
        'doctor_name': doctor_name,
        'service_account_email': 'banao-event@banao-429012.iam.gserviceaccount.com',
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [doctor_email],
        html_message=message
    )

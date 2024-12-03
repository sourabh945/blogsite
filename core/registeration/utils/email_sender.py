import asyncio
# from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import sync_to_async

import smtplib
from email.message import EmailMessage

def send_mail(subject,message,to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to
    msg.set_content(message)
    print(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    with smtplib.SMTP_SSL(settings.EMAIL_HOST, smtplib.SMTP_SSL_PORT) as smtp:
        try:
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            smtp.send_message(msg)
        except Exception as error:
             print(error)
             raise error

# Async function to send email
async def send_email_async(subject, message, recipient):
    # Run the synchronous send_mail function asynchronously
    await sync_to_async(send_mail)(
        subject=subject,
        message=message, 
        to=recipient
    )

# Simple view to trigger email sending
def send_verification_email(user_email:str,verificationLink:str):

        # Get user email from the POST data
        subject = "Email Verification"
        message = f"Please click the following link to verify your email.\n Link : {verificationLink}"

        # Call the async email sending function
        asyncio.run(send_email_async(subject, message, user_email))

        return True


send_verification_email('sourabhsheokand945@gmail.com','abc.com')
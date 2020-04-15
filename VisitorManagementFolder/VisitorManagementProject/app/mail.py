from django.core.mail import send_mail

send_mail('Subject here', 'here is the message', 'harshitaagarwal219@gmail.com', ['aharshita31@gmail.com'], fail_silently=False)

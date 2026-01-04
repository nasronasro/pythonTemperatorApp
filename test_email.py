from django.core.mail import send_mail

send_mail(
    "✅ Test Django SMTP",
    "Email de test depuis Django.",
    "boullilsouhil@gmail.com",
    ["luciferbowlil@gmail.com"],
    fail_silently=False,
)

print("✅ Email envoyé")

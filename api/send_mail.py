from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse

import datetime

class EmailContent:
    def __init__(self, request, user, token) -> None:
        self.request, self.user, self.token = request, user, token
        self.domain = get_current_site(self.request)
        
    def setup_content(self):
        verify_link = reverse("auth-api:verify-email")
        absolute_url = f"http://{self.domain}{verify_link}?token={str(self.token)}"
        exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        
        email_body = f"Hi {self.user.username}\nYou have until -{exp_date.time()}- to verify your account\n{absolute_url}"
        data = {
            "body": email_body, "subject": "Email verifying",
            "from_email": "techteam@RealEstate.com", "to": [self.user.email, ],
        }
        
        return data
    
    def reset_password_content(self):
        verify_link = reverse("auth-api:reset-password")
        absolute_url = f"http://{self.domain}{verify_link}?token={str(self.token)}"
        exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        
        email_body = f"Hi {self.user.username}\n You have until -{exp_date.time()}- to reset your password\n{absolute_url}"
        data = {
            "body": email_body, "subject": "Password Reset",
            "from_email": "techteam@RealEstate.com", "to": [self.user.email, ],
        }
        
        return data


def send_email(data):
    email = EmailMessage(**data)
    email.send()

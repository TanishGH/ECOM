from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse



class User(AbstractUser):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Vendor'),
        (2, 'Customer'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.username
    
    def is_admin(self):
        return self.role == 0
    
    def is_vendor(self):
        return self.role == 1
    
    def is_customer(self):
        return self.role == 2
    
    def generate_verification_token(self):
        """Generate a unique verification token"""
        # token = get_random_string(length=32)  # remove the comment once you add the email credientials.
        token = 'test_verification_xyz_str'
        self.email_verification_token = token
        self.save()
        return token
    
    def send_verification_email(self, request):
        try:
            token = self.generate_verification_token()
            verification_url = request.build_absolute_uri(
                reverse('users:verify_email', kwargs={'token': token})
                )
            print('verification_url>>>>>>>>>>>>>>', verification_url)
            subject = 'Verify your email address'
            message = f'''
            Hello {self.username},
            
            Please click the following link to verify your email address:
            {verification_url}
            
            If you didn't create an account, please ignore this email.
            '''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=True,
            )
            return True
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            # You might want to log this error properly
            return True
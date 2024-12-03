from django.db import models
from django.contrib.auth.models import AbstractBaseUser

### other django imports
from django.core.mail import send_mail
from django.utils.timezone import now

### settings import 

from django.conf import settings

### python simple modules import 

from uuid import uuid5
from datetime import timedelta


# Create your models here.

## import form utils 

from .utils import UserManager


class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='author email address',
        unique=True,
        max_length=126,
        error_messages={
            'unqiue':'Author with this email address already exists'
        }
    )

    username = models.CharField(
        verbose_name='username of the author',
        max_length=126,
        unique=True,
        primary_key=True,
        error_messages={
            'unique':'Author with this username already exists'
        }
    )

    name = models.CharField(
        verbose_name='name of user',
        max_length=126,
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(
        verbose_name='email verified',
        default=False,
        
    )

    ### this tags is for implimentation of LLMs

    tags = models.JSONField(
        verbose_name='tags for blog that user like',
        default=list,
        blank=True
    )
    
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self,subject,message,from_email=None,**kwargs):
        """ sending the email to the user """
        send_mail(subject,message,from_email,[self.email],**kwargs)

    def verified(self):
        """ to set the varification true"""
        self.verified_user = True
        self.save()

    def send_verificationURL(self,verificationURL:str):
        """ for verification email to the user """
        message = f'Welcome there,\n I personally welcome you to start using our blog service\n\nFor verification please click on the link :{verificationURL}\n Thank you.\nWe love to have you.\nRegards:\nSourabh Sheokand\nMaintainer of the wesite.\n'
        subject = 'Verification for Portfolio website'
        try:
            self.email_user(subject,message,settings.EMAIL_HOST_USER,fail_silently=False)
            return True
        except: 
            return False
        

class Blog(models.Model):

    id = models.AutoField(
        verbose_name='id of the blog',
        primary_key=True
    )

    title = models.CharField(
        verbose_name='title',
        blank=False,
        null=False,
        max_length=250,
    )

    author = models.ForeignKey(
        to=User,
        verbose_name='author username',
        on_delete=models.CASCADE,
        related_name='author'
    )

    date_of_pub = models.DateField(
        verbose_name='date of publication',
        auto_now_add=True
    )

    content = models.TextField(
        verbose_name='content of the blog',
        blank=False,
        null=False,
        max_length=5000
    )

    ### add the default function as the ai api function that calculates the flags take top 5 at max

    """
    """

    tags = models.JSONField(
        verbose_name='tags of the blog',
        default=list,
        blank=True
    )



### System modeles: These models are use for store the system variable for short time period only 

### please don't change any thing here whole system can f*cked up 


class ValidationIDs(models.Model):

    id = models.UUIDField(
        verbose_name='verification code',
        default=uuid5,
        unique=True,
        primary_key=True,
    )

    time_of_creation = models.DateTimeField(
        verbose_name='time of creation',
        auto_now_add=True
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )


    def validate(self,user:User) -> bool:
        if now - self.time_of_creation > timedelta(minutes=15):
            self.delete()
            return False
        if self.user == user:
            self.delete()
            return True
        return False
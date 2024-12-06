from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.dispatch import receiver

### other django imports
from django.utils.timezone import now

### settings import 

from django.conf import settings

## import from utils 

from .utils import UserManager

### import from the llm 

from .llm import get_tags


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

    
    def verified(self):
        """ to set the varification true"""
        self.verified_user = True
        self.save()




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

    date_of_pub = models.DateTimeField(
        verbose_name='date of publication',
        auto_now_add=True
    )

    content = models.TextField(
        verbose_name='content of the blog',
        blank=False,
        null=False,
        max_length=5000
    )

    tags = models.JSONField(
        verbose_name='tags',
        blank=True,
    )

# @receiver(signal=models.signals.pre_save,sender=Blog)
# def set_tags(sender,instance,*args,**kwargs):
#     if not instance.tags:
#         instance.tags = get_tags(instance.content)



"""
this file contain all the models manager we using  

"""
from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError , PermissionDenied


### local imports 

from . import validators

class CustomeUserManager(BaseUserManager):
    """
        Custome class for manage_user
    """

    def create_user(self,email:str,name:str,username:str,password:str,*args,**kwargs):
        """
        This function is for creating the user
        """
        
        if not email or not username or not name:
            raise ValidationError('All fields are required')
        
        if not validators.validate_str(username):
            raise ValidationError('Username is invalid')
        
        email = self.normalize_email(email)

        user = self.model(email=email,name=name,username=username,*args,**kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self):
        raise PermissionDenied('One one can create the super user')
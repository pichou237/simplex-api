from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("please enter a valid email address"))
        
    def create_user(self, email, first_name, last_name, password, **kwargs):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("an email address is required"))
        
        if not first_name:
            raise ValueError(_("first name is required"))
        
        if not last_name:
            raise ValueError(_("last name is required"))
        
        user = self.model(email=email, first_name=first_name, last_name=last_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_admin(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password)
        user.admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, first_name, last_name, password, organization_name="default", **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_verified", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(_("is staff must be true for admin user"))
        
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be true for admin user"))
        
        user = self.create_user(
            email, first_name, last_name, password, **kwargs
        )
        user.save(using=self._db)

        return user

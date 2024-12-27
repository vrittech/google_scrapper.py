from django.db import models
from django.db import models
from .utilities.model_utils import LowercaseEmailField
from django.contrib.auth.models import AbstractUser
from .roles import roles_data,roles_data_dict
from .import roles
from subscriptionplan.models import SubscriptionPlan
import uuid
from django.db.models import Sum
from datetime import date
from .utilities.validators import validate_emails, validate_mobile_number
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    phone = models.CharField(max_length=15,null=True , default = '')
    email = LowercaseEmailField(
            _("email address"),
            unique=True,
            validators=[validate_emails],
            error_messages={"unique": "Given Email has already been registered."},
            null=True,
            blank=True,
        )
    
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True,default=None)
    api_usage = models.PositiveIntegerField(default=0)
    api_limit = models.PositiveIntegerField(default=100)  # Default to free tier
    is_commercial_user = models.BooleanField(default=False)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    plan_renewal_date = models.DateTimeField(null=True, blank=True)
    last_reset_date = models.DateField(default=date.today)
    account_status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Suspended', 'Suspended'),
            ('Canceled', 'Canceled')
        ],
        default='Active'
    )
    
    username = models.CharField(max_length=255,unique=True)  

    full_name = models.CharField(null = True,default = '')  
    dob = models.DateField(null= True,blank= True ) 

    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200,null=True,default = '')

    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
 
    image = models.ImageField(upload_to="profiles/images",default=None,null=True,blank=True)
    role = models.PositiveSmallIntegerField(choices=roles_data, blank=True, null=True,default = 5)

    system_provider = 1
    google_provider = 2
    facebook_provider = 3

    old_password_change_case = models.BooleanField(default=True) 

    provider_CHOICES = (
        (system_provider, 'system'),
        (google_provider, 'google'),
        (facebook_provider, 'facebook'), 
        (4, 'apple'), 

    )
    provider = models.PositiveSmallIntegerField(choices=provider_CHOICES,default = system_provider)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def getRoleName(self):
        if self.role==roles.SUPER_ADMIN:
            return roles_data_dict[roles.SUPER_ADMIN]
        elif self.role == roles.ADMIN:
            return roles_data_dict[roles.ADMIN]
        elif self.role == roles.USER:
            return roles_data_dict[roles.USER]
        else:
            return None
        
    def __str__(self):
        return self.username + " "+ str(self.getRoleName())
    
    def reset_usage(self):
        """
        Reset API usage for the new month.
        """
        today = date.today()
        if self.last_reset_date.month != today.month:
            self.api_usage = 0
            self.last_reset_date = today
            self.save()
    
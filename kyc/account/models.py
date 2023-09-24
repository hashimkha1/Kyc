from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.db.models.signals import post_save



ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("inactive", "Inactive")
)

MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)

     # For CIPCompliance

class CIPCompliance(models.Model):
    # customer = models.OneToOneField(on_delete=models.CASCADE)
    date_of_check = models.DateTimeField(auto_now_add=True)
    compliance_status = models.CharField(max_length=20, choices=[('Passed', 'Passed'), ('Failed', 'Failed')])
    compliance_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"CIP Compliance for {self.customer}"    
#   KYC MODEL
class KYC(models.Model):
    id=models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4,editable=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # account=models.OneToOneField(Account, on_delete=models.CASCADE,null=True,blank=True)
    full_name=models.CharField(max_length=1000)
    image=models.ImageField(upload_to="kyc",default="default.jpg")
    marital_status=models.CharField(choices=MARITAL_STATUS,max_length=50)
    gender=models.CharField(choices=GENDER,max_length=50)
    identity_type=models.CharField(choices=IDENTITY_TYPE,max_length=150)
    identity_image=models.ImageField(upload_to="kyc",null=True,blank=True)
    date_of_birth=models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc")

    # Address
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)


    # Contact Detail
    mobile=models.CharField(max_length=500)
    fax=models.CharField(max_length=500)
    date=models.DateTimeField(auto_now_add=True)


    # Risk Assessment
    risk_rating = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='low')

    cip_compliance = models.OneToOneField(CIPCompliance, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['-date']

       

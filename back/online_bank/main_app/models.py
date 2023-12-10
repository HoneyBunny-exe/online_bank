from django.db import models
from utils import custom_validators


class User(models.Model):
    first_name = models.TextField()
    second_name = models.TextField()
    third_name = models.TextField()
    phone_code = models.CharField(max_length=3, validators=[custom_validators.validate_phone_code])
    phone_number = models.CharField(max_length=14, validators=[custom_validators.validate_phone_number])
    email = models.EmailField(null=True)
    other_info = models.JSONField()


class Authorization(models.Model):
    login = models.CharField(max_length=255, primary_key=True)
    password = models.BinaryField()
    salt = models.BinaryField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='auth_user')

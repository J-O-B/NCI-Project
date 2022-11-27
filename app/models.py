from hashlib import sha256
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid, datetime, base64, random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Pending(models.Model):
    """
    If a user trys to access from a device, or IP that is not linked with their profile,
    they will be asked if they want to add the device / IP. If they choose yes, an email 
    will be sent to their email to confirm. The IP and / or device will be saved as pending
    until they confirm. 
    URL Endpoint should include the ID of the pending class
    """
    def gen_end():
        chars = "abcdefghijklmnopqrstuvwxyz1234567890"
        out = ""
        for i in range(50):
            out += random.choice(chars)
        return out

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    save_type = models.CharField(max_length=6, blank=False, null=False)
    data = models.TextField(max_length=4086, null=True, blank=True)
    endpoint = models.CharField(default=gen_end(), max_length=55, null=False)

class IPModel(models.Model):
    """
    The IPModel will store IPs. These can be added as a foreign key to a user account.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.CharField(max_length=46, blank=False, null=False)

    def __str__(self):
        return str(self.ip)

class Device(models.Model):
    """
    The Device Model will store Device headers. These can be added as a foreign key to a user 
    account.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=1024, null=False, blank=False)

    def __str__(self):
        return str(self.info)

class Credential(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=85, blank=True, null=True)
    password = models.CharField(max_length=85, blank=True, null=True)
    phone = models.CharField(max_length=85, blank=True, null=True)
    email = models.CharField(max_length=85, blank=True, null=True)
    
    def __str__(self):
        return str(self.service)

class UserProfile(models.Model):
    def gen_key():
        password_gen = uuid.uuid4
        password = str(password_gen).encode()
        salt = str(password_gen) + '_'
        salt = salt.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=50000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password)).decode()
    
    def user_pin():
        allowed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        pin = f'{random.choice(allowed)}{random.choice(allowed)}{random.choice(allowed)}{random.choice(allowed)}'
        return pin
        

    userid = models.CharField(max_length=85, default=gen_key(), editable=False)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    pin = models.CharField(default=user_pin(), max_length=4, blank=False, null=False, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.datetime.now, editable = False)
    phone = models.CharField(max_length=50, blank=True, null=True)
    devices = models.ManyToManyField(Device, blank=True)
    ips = models.ManyToManyField(IPModel, blank=True)
    credentials = models.ManyToManyField(Credential, blank=True)
    
    def __str__(self):
        return str(self.name)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.get_or_create(user=instance)
        except:
            pass
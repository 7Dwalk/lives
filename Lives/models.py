from django.contrib.auth.models import AbstractUser
from django.db import models


class Message(models.Model):
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    video = models.FileField(upload_to='video/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    text = models.TextField()
    delivery_time = models.DateTimeField()
    sender_hidden_parameter = models.CharField(max_length=100)
    recipient_hidden_parameter = models.CharField(max_length=100)
    identification_number = models.CharField(max_length=25)

    def __str__(self):
        return self.text


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def create_profile(self, profile_name):
        profile = Profile.objects.create(name=profile_name, user=self)
        return profile

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def change_email(self, new_email):
        self.email = new_email
        self.save()


class Profile(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()

    def change_username(self, new_username):
        self.username = new_username
        self.save()

    def change_password(self, new_password):
        self.password = new_password
        self.save()

    def change_email(self, new_email):
        self.email = new_email
        self.save()

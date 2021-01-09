from django.db import models
from django.urls import reverse


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, primary_key=True)
    password = models.CharField(max_length=100)
    invited = models.BooleanField()

    def __str__(self):
        return self.email


class WorkSpace(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=30)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.name


class UserWorkSpace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    privilege = models.BooleanField("is admin")


class UserChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)




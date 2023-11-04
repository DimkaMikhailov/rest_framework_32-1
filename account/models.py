from django.db import models
from django.contrib.auth.models import User


class AccessKey(models.Model):
    key = models.CharField(max_length=8)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='access_key')
    create_time = models.DateTimeField(auto_now_add=True)





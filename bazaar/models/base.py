from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    def get_admin(self):
        user = User.objects.get(username='admin')
        return user

    # TODO
    def save(self, *args, **kwargs):
        self.x_user = self.get_admin()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

from django.db import models
from django.conf import settings
from smart_selects.db_fields import ChainedForeignKey
from django_celery_beat.models import PeriodicTask
from datetime import timedelta
import requests
import uuid
import math

class Message(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    schedule = models.ForeignKey(PeriodicTask, blank=True, null=True, default='',on_delete=models.PROTECT)
    bot_message = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return "%s " %self.title
    def human_readable(self):
    	return self.schedule.crontab.human_readable

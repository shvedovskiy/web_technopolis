from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime


class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    file = models.FileField()
    # image = models.ImageField()  # Pillow package required

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

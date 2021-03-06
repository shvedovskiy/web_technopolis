from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class Post(models.Model):
    class Meta:
        db_table = 'post'
        verbose_name = u'Запись'
        verbose_name_plural = u'Записи'
        ordering = ('-created_date',)

    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    # likes = models.ManyToManyField(User, related_name='likes')

    #@property
    #def total_likes(self):
    #    return self.likes.count()

    def get_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        db_table = 'comment'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey('auth.User')
    text = models.TextField(verbose_name='Comment text')
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

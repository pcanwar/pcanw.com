import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


def getFileName(filePath):
    base_name = os.path.basename(filePath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_file = uuid.uuid4()
    name, ext = getFileName(filename)
    final_name = '{newFile}{ext}'.format(newFile=new_file, ext=ext)
    return "blog/{newFile}{finalname}".format(newFile=new_file,
                                              finalname=final_name)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    tags = TaggableManager()

    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=450,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    image = models.ImageField(upload_to=upload_image_path,
                              blank=True, null=True)

    description = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return str(self.uuid)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       # args=[str(self.id)])
                       kwargs={'uuid': str(self.uuid)})

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                    args=[self.publish.year,
    #                          self.publish.month,
    #                          self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from tinymce import HTMLField

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
            upload_to='profile_images/',
            null=True,
            blank=True
    )

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={
            'category': slugify(self.title)
        })

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Image(models.Model):
    image = models.ImageField(upload_to='post_images/')
    alt_tag = models.CharField(
        max_length=125,
        help_text='Describe the image in a specific manner',
        blank=True
    )

    def __str__(self):
        return self.image.name


class Post(models.Model):
    '''
    This title is used for page title
    and is limited to 60 chracters for better SEO
    '''
    title = models.CharField(
        max_length=60,
        help_text='Try placing important keywords first'
    )
    slug = models.SlugField()
    description = models.CharField(
        max_length=160,
        help_text='Description of your post'
    )
    content = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    categories = models.ManyToManyField(Category, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'slug': self.slug
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'slug': self.slug
        })

    def Meta(self):
        ordering = ['-timestamp']  # noqa: F841

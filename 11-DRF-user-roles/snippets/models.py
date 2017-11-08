from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.http import Http404

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)


class Role(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=254)


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, related_name='snippets', null=True)

    # def save(self, *args, **kwargs):
    #     print ('---> User----- SAVE: ', self, args, kwargs)
    #     super(User, self).save(*args, **kwargs)
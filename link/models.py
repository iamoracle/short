from django.db.models import Model

# Create your models here.

class Link(Model):

    link = URLField(max_length=1024)

    slug = SlugField(max_length=16)
from django.db.models import Model, SlugField, URLField, UUIDField

from uuid import uuid4

from .helpers import uuid

from .validators import url_exists

class Link(Model):

    """[summary] the database representation of a link
    """

    url = URLField(max_length=1024, validators=(url_exists,))
    """[summary] this represents the link the  
    """

    slug = SlugField(max_length=16, default=uuid, unique=True)
    """[summary] this slug or shortened version of the link  
    """

    secret = UUIDField(default=uuid4)
    """[summary] user must provide this secret when they want to delete the link """
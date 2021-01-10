from rest_framework.serializers import ModelSerializer

from .models import Link

class LinkSerializer(ModelSerializer):

    """[summary] this represents the database model in a json format
    """

    model = Link
    """[summary] the model to serialized
    """

    fields = '__all__'
    """[summary] serialize all fields
    """

    read_only_fields = ('secret',)
    """[summary] secret fields should only be read only to avoid tampering with it!
    """
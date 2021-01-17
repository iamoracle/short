from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView

from rest_framework.views import APIView

from .serializers import LinkSerializer, PublicLinkSerializer

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from requests import post

from requests.exceptions import RequestException

import json

from django.shortcuts import get_object_or_404

from .models import Link

from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from rest_framework.response import Response

import environ

# environment loader initializer for security
env = environ.Env()

# start loading the variables into memory
environ.Env.read_env()


class LinkView(CreateAPIView, DestroyAPIView, RetrieveAPIView):

    """[summary] this view provides support for adding and deleting a link \n
        extending CreateAPIView provides us with functionalities to add a link \n
        extending DestroyAPIView provides us with functionalities to delete a link
    """

    # permission_classes = (IsAuthenticated,)

    """[summary] uncomment if you want to make sure only authenticated users can use this app
    """

    def get_queryset(self):

        """[summary] This method provides a Queryset of all links
        """

        return Link.objects.all()

    def get_serializer_class(self, *args, **kwargs):

        serializers = {
            'POST': LinkSerializer,
            'DELETE': LinkSerializer,
            'GET': PublicLinkSerializer
        }

        return serializers.get(self.request.method)

    def get_object(self):

        """[summary] Get a particular object/item from link \n
            copied from the official django rest_framework website
        """

        queryset = self.get_queryset()

        # check for the secret if user wants to do something funny
        # i.e delete link

        if not self.request.method in SAFE_METHODS:

            slug = self.request.data.get('slug', None)

            secret = self.request.data.get('secret', None)

            filter = {
                'slug': slug,
                'secret': secret
            }

        else:

            slug = self.request.GET.get('slug', None) or self.request.data.get('slug', None)

            filter = {
                'slug' : slug
            }

        # inbuilt django used

        obj = get_object_or_404(queryset, **filter)

        self.check_object_permissions(self.request, obj)

        return obj
    

    def post(self, request, *args, **kwargs):

        """[summary] add a new link
        """
        
        # hcaptcha doesn't work on localhost, therefore, we are going to use it only
        # when we go live!
        if env('USE_HCAPTCHA') == "True":

            # Retrieve token from post data with key 'h-captcha-response'.
            token = request.data.get('h-captcha-response', False)

            # if the token is False that means token is empty
            if not token:

                message = {'h-captcha-response': 'hcaptcha token is empty'}

                return Response(message, status=HTTP_400_BAD_REQUEST)

            # Build payload with secret key and token.
            data = {'secret': env('HCAPTCHA_SECRET_KEY'), 'response': token}

            # we can't trust our request to go through 100% of the time
            # so we will try and catch errors as they happen
            try:

                # Make POST request with data payload to hCaptcha API endpoint.
                response = post(url=env('HCAPTCHA_VERIFY_URL'), data=data)

            except RequestException:

                message = {
                    'h-captcha-response': 'unknown error while processing hcaptcha token'}

                return Response(message, status=HTTP_400_BAD_REQUEST)

            # Parse JSON from response.
            response = response.json()

            # Check for success or error codes.
            # Note success can either be True or False
            success = response['success'] or False

            # only if successful call django restframework create method
            if not success:

                message = {'h-captcha-response': 'invalid hcaptcha token'}

                return Response(message, status=HTTP_400_BAD_REQUEST)

        # initiate the create request
        return self.create(request, *args, **kwargs)

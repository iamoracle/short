from requests import get

from requests.exceptions import RequestException

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

def url_exists(url):

    try:

        response = get(url)

    except RequestException:

        raise ValidationError(_('invalid or inactive url'))

    status = response.status_code

    if status >= 200 and status < 300: return True
    
    else: raise ValidationError(_('url does not exists'))

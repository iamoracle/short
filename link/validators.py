from requests import get

from requests.exceptions import RequestException

def url_exists(url):

    try:

        response = requests.get(url)

    except RequestException:

        return False

    status = response.status_code

    return status >= 200 and status < 300

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def html_get(url):
    """
    Gets the content at `url` by making an HTTP GET request.
    If the content-type of the response is HTML, return the text content, otherwise return None.
    """
    try:
        with closing(get(url, stream = True)) as response:
            if is_html(response):
                return response.content
            else:
                return None

    except RequestException as e:
        print('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_html(response):
    """
    Returns True if the response is HTML, false otherwise.
    """
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
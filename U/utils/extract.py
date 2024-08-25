from urllib.request import urlopen 
from urllib.error import HTTPError

def get_filename_from_url(url):
    try:
        response = urlopen(url)
        filename = response.headers.get_filename()
        if filename:
            return filename
    except HTTPError:
      return None

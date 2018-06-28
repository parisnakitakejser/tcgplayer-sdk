import requests
import json


class Products:
    __token = None

    def __init__(self, token=None):
        self.__token = token

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__token = None

    def __header(self):
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'bearer {token}'.format(token=self.__token),
            'Connection': 'close'
        }
        return headers

    def get(self, product_condition_ids=[]):
        request_url = 'http://api.tcgplayer.com/v1.8.1/pricing/sku/{product_condition_ids}'.format(product_condition_ids=(','.join(product_condition_ids)))
        try:
            response = requests.get(request_url, headers=self.__header(), timeout=3)
            result = json.loads(response.text)

            return result['results']
        except requests.exceptions.ReadTimeout as timeout:
            print(request_url)
            return False

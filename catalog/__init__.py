import requests
import json


class Categories:
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

    def search(self, category_id=1, product='', category=''):
        data = {
            'filters': []
        }

        if category != '':
            data['filters'].append({
                'name': 'Category',
                'values': [category]
            })

        if product != '':
            data['filters'].append({
                'name': 'ProductName',
                'values': [product]
            })

        request_url = 'http://api.tcgplayer.com/catalog/categories/{category_id}/search'.format(category_id=category_id)
        try:
            response = requests.post(request_url, headers=self.__header(), data=json.dumps(data), timeout=3)
            resualt = json.loads(response.text)

            return resualt
        except requests.exceptions.ReadTimeout as timeout:
            print(request_url)
            return False


class Products:
    __token = None
    __products = []

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
        }
        return headers

    def find(self, product_ids=[]):
        request_url = 'http://api.tcgplayer.com/v1.8.0/catalog/products/{product_id}'.format(product_id=(','.join(product_ids)))

        try:
            response = requests.get(request_url , headers=self.__header(), timeout=3)
            result = json.loads(response.text)

            self.__products = result['results']
            return True
        except requests.exceptions.ReadTimeout as timeout:
            print(request_url)
            return False

    def product_conditions(self):
        data = {}
        for row in self.__products:
            conditions_data = {}

            for conditions in row['productConditions']:
                if conditions['language'] not in conditions_data:
                    conditions_data[conditions['language']] = {
                        'foil': [],
                        'normal': []
                    }

                if conditions['isFoil'] is True:
                    conditions_data[conditions['language']]['foil'].append({
                        'id': conditions['productConditionId'],
                        'name': (conditions['name'].split(' - '))[0],
                    })
                else:
                    conditions_data[conditions['language']]['normal'].append({
                        'id': conditions['productConditionId'],
                        'name': (conditions['name'].split(' - '))[0],
                    })

            data[row['productId']] = conditions_data

        return data

    def product_condition_ids(self):
        data = {}
        for row in self.__products:
            conditions_data = []

            for conditions in row['productConditions']:
                conditions_data.append(conditions['productConditionId'])

            data[row['productId']] = conditions_data

        return data

    def product_group(self):
        data = {}
        for row in self.__products:
            data[row['productId']] = {
                'id': row['group']['groupId'],
                'name': row['group']['name'],
                'code': row['group']['abbreviation'],
                'supplemental': row['group']['supplemental'],
                'published': row['group']['publishedOn'],
                'last-modified': row['group']['modifiedOn'],
                'category': {
                    'id': row['group']['category']['categoryId'],
                    'name': row['group']['category']['name'],
                    'last-modified': row['group']['category']['modifiedOn']
                }
            }

        return data

    def get(self):
        return self.__products

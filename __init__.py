import requests, json

class Token:
    __client_id = None
    __client_secret = None

    token_key = None
    token_type = None
    token_expires = None

    def __init__(self, client_id=None, client_secret=None):
        self.__client_id = client_id
        self.__client_secret = client_secret

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__client_id = None
        self.__client_secret = None

    def request(self):
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Connection': 'close'
        }

        data = 'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'.format(client_id=self.__client_id, client_secret=self.__client_secret)
        response = requests.post('https://api.tcgplayer.com/token', headers=headers, data=data, timeout=3)

        data = json.loads(response.text)

        self.token_key = data['access_token']
        self.token_type = data['token_type']
        self.token_expires = data['.expires']
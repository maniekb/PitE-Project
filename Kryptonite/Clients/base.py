import requests


class BaseClient:
    def __init__(self, url):
        self.base_url = url

    def get(self, param):
        response = requests.get(url=self.base_url, params=param)
        return response.json()

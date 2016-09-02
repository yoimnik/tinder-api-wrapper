import requests
import json
import datetime
import sys


class TinderClient:
    api_url = 'https://api.gotinder.com'


    def __init__(self, facebook_token, facebook_id):
        request = {
            'facebook_token': facebook_token,
            'facebook_id': facebook_id,
            'locale': 'en'
        }

        try:
            response = requests.post(self.api_url + '/auth', data=request)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print e
            sys.exit(1)

        data = json.loads(response.text)
        self.api_token = data['token']
        self.full_name = data['user']['full_name']
        self.distance_filter = data['user']['distance_filter']


    def popular_locations(self):
        request = {
            'locale': 'en'
        }

        response = requests.get(self.api_url + '/location/popular', data=json.dumps(request), headers=self._headers(False))
        return json.loads(response.text)


    def fetch_updates(self):
        request = {
            'last_activity_date': datetime.datetime.now().isoformat()
        }

        response = requests.post(self.api_url + '/updates', data=json.dumps(request), headers=self._headers(True))
        return json.loads(response.text)


    def profile_meta(self):
        response = requests.get(self.api_url + '/meta', headers=self._headers(False))
        return json.loads(response.text)


    def nearby_users(self):
        response = requests.get(self.api_url + '/user/recs', headers=self._headers(False))
        return json.loads(response.text)


    def swipe_right(self, user_id):
        response = requests.get(self.api_url + '/like/' + user_id, headers=self._headers(False))
        return json.loads(response.text)


    def swipe_left(self, user_id):
        response = requests.get(self.api_url + '/pass/' + user_id, headers=self._headers(False))
        return json.loads(response.text)


    def super_like(self, user_id):
        response = requests.post(self.api_url + '/like/' + user_id + '/super', headers=self._headers(True))
        return json.loads(response.text)


    def _headers(self, post):
        headers = {
            'platform': 'android',
            'X-Auth-Token': self.api_token,
            'User-Agent': 'Tinder Android Version 5.3.4',
            'os-version': 21,
            'Accept-Language': 'en',
            'app-version': 1625,
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        if post:
            headers['Content-Type'] = 'application/json; charset=utf-8'
        return headers

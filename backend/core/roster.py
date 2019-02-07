from __future__ import print_function

# for login
import requests
import requests.auth
import urllib
import json

# for ednudge_api
import time
import ednudge_api
from ednudge_api.rest import ApiException
from pprint import pprint

from .models import District
import logging

USER_EMAIL="chris.whiteley@billboard.net"
USER_PASSWORD="1234567890"
EDNUDGE_PROTOCOL="https"

EDNUDGE_PORT="443"
EDNUDGE_API_VERSION="api/v1"

logger = logging.getLogger(__name__)

class Roster:

    config = ""
    api_instance = ""
    ednudge_host = ""
    ednudge_api_url = ""

    def __init__(self, ednudge_host):
        self.ednudge_host = 'https://{}'.format(ednudge_host)
        self.ednudge_api_url='{}/{}/'.format(self.ednudge_host, "api/v1")
        logger.debug("ednudge_host=%s ednudge_api_url=%s", self.ednudge_host, self.ednudge_api_url)

        token = self.login()
        self.config = ednudge_api.Configuration()
        self.config.host = self.ednudge_host
        self.config.debug=True
        self.config.api_key['Authorization']=token
        self.config.api_key_prefix['Authorization']='Bearer'
        self.api_instance = ednudge_api.RosterApiApi(ednudge_api.ApiClient(self.config))        

    def login(self):
        params = {
            "grant_type": "password",
            "client_id": "not implemented",
            "client_secret": "not implemented",
            "email": USER_EMAIL,
            "password": USER_PASSWORD
        }

        token = ""

        try:
            endpoint = '{}login'.format(self.ednudge_api_url)
            my_json = json.dumps(params)
            r = requests.post(endpoint, json=params)
            r.raise_for_status()
            logger.debug('response: {}'.format(r.text))
            token = r.json()['token']

        except requests.exceptions.HTTPError as e:
            logger.exception('HTTP error: {}'.format(e))

        except requests.exceptions.RequestException as e:
            logger.exception('Other Error: {}'.format(e))

        logger.debug('token: {}'.format(token))
        return token

    def get_districts(self):
        data = None
        try:
            data = self.api_instance.api_v1_districts_get()
            logger.debug("EdNudge Districts: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_districts_get: %s\n" % e)

        ah_districts = District.objects.values_list()
        print(ah_districts)


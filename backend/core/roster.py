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

EDNUDGE_API_VERSION="api/v1"

logger = logging.getLogger(__name__)

class Roster:

    config = ""
    api_instance = ""
    ednudge_host = ""
    ednudge_api_url = ""

    def __init__(self, ednudge_host, username, password):
        self.ednudge_host = ednudge_host
        ednudge_api_version=EDNUDGE_API_VERSION
        self.ednudge_api_url=f"{self.ednudge_host}/{ednudge_api_version}/"
        logger.debug("ednudge_host=%s ednudge_api_url=%s", self.ednudge_host, self.ednudge_api_url)

        token = self.login(username, password)
        self.config = ednudge_api.Configuration()
        self.config.host = self.ednudge_host
        self.config.debug=True
        self.config.api_key['Authorization']=token
        self.config.api_key_prefix['Authorization']='Bearer'
        self.api_instance = ednudge_api.RosterApiApi(ednudge_api.ApiClient(self.config))        

    def login(self, username, password):
        params = {
            "grant_type": "password",
            "client_id": "not implemented",
            "client_secret": "not implemented",
            "username": username,
            "password": password
        }

        token = ""

        try:
            endpoint = '{}login'.format(self.ednudge_api_url)
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

    def ednudge_get_districts(self):
        data = None
        try:
            data = self.api_instance.api_v1_districts_get()
            logger.debug("EdNudge Districts: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_districts_get: %s\n" % e)
        return data

    def ednudge_get_schools(self, district_id):
        data = None
        try:
            data = self.api_instance.api_v1_districts_id_schools_get(district_id)
            logger.debug("EdNudge Schools: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_schools_get: %s\n" % e)
        return data

    def ednudge_get_sections(self, district_id):
        data = None
        try:
            data = self.api_instance.api_v1_districts_id_sections_get(district_id)
            logger.debug("EdNudge Sections: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_districts_id_sections_get: %s\n" % e)
        return data

    def ednudge_get_enrollments(self, district_id, skip, limit, school_id=None):
        data = None
        try:
            if school_id:
                data = self.api_instance.api_v1_districts_id_enrollments_get(district_id, skip=skip, limit=limit, school_id__eq=school_id)
            else:
                data = self.api_instance.api_v1_districts_id_enrollments_get(district_id, skip=skip, limit=limit)
            logger.debug("EdNudge Enrollments: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_districts_id_enrollments_get: %s\n" % e)
        return data

    def ednudge_get_learners(self, district_id):
        data = None
        try:
            data = self.api_instance.api_v1_districts_id_learners_get(district_id, limit=24000)
            #data = self.api_instance.api_v1_learners_get()
            logger.debug("EdNudge Learners: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_districts_id_learners_get: %s\n" % e)
        return data

    def ednudge_get_instructors(self, district_id):
        data = None
        try:
            data = self.api_instance.api_v1_districts_id_instructors_get(district_id, limit=20000)
            #data = self.api_instance.api_v1_instructors_get()
            logger.debug("EdNudge Instructors: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_districts_id_instructors_get: %s\n" % e)
        return data

    def ednudge_get_dailyattendance(self, district_id):
        data = None
        try:
            data = self.api_instance.api_v1_districts_id_daily_attendance_get(district_id)
            #data = self.api_instance.api_v1_districts_id_daily_attendance_get()
            logger.debug("EdNudge DailyAttendance: {}".format(data.data))
        except ApiException as e:
            logger.exception("Exception when calling DefaultApi->api_v1_districts_id_daily_attendance_get: %s\n" % e)
        return data

    def ednudge_get_guardians(self, district_id):
        data = None
        try:
            data = self.api_instance.api_v1_districts_id_guardians_get(district_id)
            logger.debug(f"EdNudge Guardians: {data.data}")
        except ApiException as e:
            logger.exception(f"Exception when calling DefaultApi->api_v1_districts_id_guardians_get: {e}\n")
        return data

    def get_api_instance(self):
        return self.api_instance
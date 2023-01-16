"""API"""

import os
import sys
import requests
sys.path.append(os.getcwd())

from constants import DockerConstants, ApiConstants


class ApiClient:
    """Bears API class"""

    def __init__(self, base_url=DockerConstants.BASE_URL):
        """ApiClient init

        :param base_url: base URL for REST requests
        :type base_url: str
        :return: None
        """
        self._base_url = base_url

    @property
    def base_url(self):
        """base_url getter

        :return: base URL address
        :rtype: str
        """
        return self._base_url

    def post_add(self, **kwargs):
        """POST REST. Create record

        :return: Response object
        :rtype: requests.models.Response
        """
        url = self.base_url + ApiConstants.POST_ADD_PATH
        return requests.post(url=url, **kwargs)

    def get_info(self, **kwargs):
        """GET REST. Get info

        :return: Response object
        :rtype: requests.models.Response
        """
        url = self.base_url + ApiConstants.GET_INFO_PATH
        return requests.get(url=url, **kwargs)

    def get_one(self, bear_id, **kwargs):
        """GET REST. Get one database record

        :param bear_id: Bear bear_id
        :type bear_id: int
        :return: Response object
        :rtype: requests.models.Response
        """
        url = self.base_url + ApiConstants.GET_ONE_PATH + str(bear_id)
        return requests.get(url=url, **kwargs)

    def get_all(self, **kwargs):
        """GET REST. Get whole database

        :return: Response object
        :rtype: requests.models.Response
        """
        url = self.base_url + ApiConstants.GET_ALL_PATH
        return requests.get(url=url, **kwargs)

    def put_one(self, bear_id, **kwargs):
        """PUT REST. Update database record

        :param bear_id: Bear bear_id
        :type bear_id: int
        :return: Response object
        :rtype: requests.models.Response
        """
        url = self.base_url + ApiConstants.PUT_ONE_PATH + str(bear_id)
        return requests.put(url=url, **kwargs)

    def delete_one(self, bear_id, **kwargs):
        """DELETE REST. Delete one record

        :param bear_id: Bear bear_id
        :type bear_id: int
        :return: Response object
        :rtype: requests.models.Response
        """
        url = self.base_url + ApiConstants.DELETE_ONE_PATH + str(bear_id)
        return requests.delete(url=url, **kwargs)

    def delete_all(self, **kwargs):
        """DELETE REST. Delete all database records

        :return: Response object
        :rtype: requests.models.Response
        """
        url = self.base_url + ApiConstants.DELETE_ALL_PATH
        return requests.delete(url=url, **kwargs)


def validate_response_code(resp_obj, code, should_be_equal=True):
    """Validate response code

    :parameter resp_obj: Response object
    :type resp_obj: requests.models.Response
    :parameter code: HTTP statuse code
    :type code: int
    :parameter should_be_equal: True -> assert resp_obj == code, False -> assert resp_obj != code,
    :type should_be_equal: int
    :return: None
    """
    if should_be_equal:
        assert resp_obj.status_code == code, 'STATUS CODE: {0}: {1}'.format(resp_obj.status_code, resp_obj.reason)
    else:
        assert resp_obj.status_code != code, 'STATUS CODE: {0}: {1}'.format(resp_obj.status_code, resp_obj.reason)

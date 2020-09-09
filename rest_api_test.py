"""
Welcome to Alaska!
This is CRUD service for bears in alaska.
CRUD routes presented with REST naming notation:

POST			/bear - create
GET		    	/bear - read all bears
GET		    	/bear/:id - read specific bear
PUT		    	/bear/:id - update specific bear
DELETE			/bear - delete all bears
DELETE			/bear/:id - delete specific bear

Example of bear json: {"bear_type":"BLACK","bear_name":"mikhail","bear_age":17.5}.
Available types for bears are: POLAR, BROWN, BLACK and GUMMY.
"""

import requests
import pytest
import copy

import sys
sys.path.append("../")

from common import REST_URL
from common import use_docker


simple_positive_json = {"bear_type": "BLACK",
                        "bear_name": "BOB",
                        "bear_age": 10.0}

bear_types_positive = ['POLAR', 'BROWN', 'BLACK', 'GUMMY']
bear_names_positive = ['bob', 'BoB', 'B', 'b', 'a'*10]
bear_ages_positive = [0.1, 1, 50, 99, 100.0, 33.33333]

bear_types_negative = ['POLAr', 'brown', 'WHITE', '!,.[]', '']
bear_names_negative = [1, 'b!', 'A@A', [], {1: 1}, 'a'*11, '']
bear_ages_negative = [-1, -1.0, 0.0, 101, 100.1, 'bob', [], {1: 1}, '']

bear_get_negative = [66666, 'a', {1: 1}, [0]]

@pytest.fixture(scope='module')
def smoke_test():
    """quick smoke check that checks basic functionality without which there is no sense to check test suit"""
    json_expected = copy.copy(simple_positive_json)

    # bear create check
    resp_post = requests.post(REST_URL + '/bear', json=json_expected)
    assert resp_post.status_code == 200
    json_expected.update({'bear_id': resp_post.json()})

    # bear get check
    resp_get = requests.get(REST_URL + '/bear/{}'.format(resp_post.json()))
    assert resp_get.status_code == 200
    json_result = resp_get.json()
    assert json_result == json_expected

    # all bears delete check
    resp_delete = requests.delete(REST_URL + '/bear')
    assert resp_delete.status_code == 200
    assert not requests.get(REST_URL + '/bear').json()

@pytest.mark.usefixtures('smoke_test')
class TestAlaska:
    """Test suit for Alaska test"""

    @pytest.mark.parametrize('bear_type', bear_types_positive, ids=bear_types_positive)
    @pytest.mark.parametrize('bear_name', bear_names_positive, ids=bear_names_positive)
    @pytest.mark.parametrize('bear_age', bear_ages_positive, ids=bear_ages_positive)
    def test_positive_create_get_bear(self, bear_type: str, bear_name: str, bear_age: int or float) -> None:
        """Positive bear POST create + GET read specific bear"""

        json_expected = {'bear_type': bear_type, 'bear_name': bear_name, 'bear_age': bear_age}
        resp_post = requests.post(REST_URL + '/bear', json=json_expected)

        assert resp_post.status_code == 200, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        json_expected.update({'bear_name': bear_name.upper(), 'bear_age': float(bear_age), 'bear_id': resp_post.json()})

        resp_get = requests.get(REST_URL + '/bear/{}'.format(resp_post.json()))
        json_result = resp_get.json()
        assert json_result == json_expected

    @pytest.mark.parametrize('bear_type', bear_types_negative,
                             ids=lambda bear_types_negative: '{}'.format(bear_types_negative))
    def test_negative_create_bear_types(self, bear_type: str) -> None:
        """Negative bear POST create. WRONG bear_type"""

        json = copy.copy(simple_positive_json)
        json.update({'bear_type': bear_type})

        resp_post = requests.post(REST_URL + '/bear', json=json)
        assert resp_post.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        assert resp_post.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)

    @pytest.mark.parametrize('bear_name', bear_names_negative,
                             ids=lambda bear_names_negative: '{}'.format(bear_names_negative))
    def test_negative_create_bear_names(self, bear_name: str) -> None:
        """Negative bear POST create. WRONG bear_name"""

        json = copy.copy(simple_positive_json)
        json.update({'bear_name': bear_name})

        resp_post = requests.post(REST_URL + '/bear', json=json)
        assert resp_post.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        assert resp_post.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)

    @pytest.mark.parametrize('bear_age', bear_ages_negative,
                             ids=lambda bear_ages_negative: '{}'.format(bear_ages_negative))
    def test_negative_create_bear_ages(self, bear_age: int or float) -> None:
        """Negative bear POST create. WRONG bear_age"""

        json = copy.copy(simple_positive_json)
        json.update({'bear_age': bear_age})

        resp_post = requests.post(REST_URL + '/bear', json=json)
        assert resp_post.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        assert resp_post.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)

    @pytest.mark.parametrize('bear_id', bear_get_negative,
                             ids=lambda bear_get_negative: '{}'.format(bear_get_negative))
    def test_negative_get_bear(self, bear_id) -> None:
        """Negative SPECIFIC bear GET read """

        resp_post = requests.get(REST_URL + '/bear/{}'.format(bear_id))
        if isinstance(bear_id, int):
            assert resp_post.status_code == 404, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        else:
            assert resp_post.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)

    def test_positive_delete_one_bear(self) -> None:
        """Positive check if Delete One bear works"""

        # create bear
        json_expected = copy.copy(simple_positive_json)
        resp_post = requests.post(REST_URL + '/bear', json=json_expected)
        bear_id = resp_post.json()
        json_expected.update({'bear_id': bear_id})
        resp_get = requests.get(REST_URL + '/bear/{}'.format(bear_id))
        json_result = resp_get.json()
        assert json_result == json_expected

        # delete bear
        resp_post = requests.delete(REST_URL + '/bear', json=json_expected)

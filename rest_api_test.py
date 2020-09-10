"""REST API Autotest"""

import requests
import pytest
import copy
import os
import sys
sys.path.append(os.getcwd())

from common import REST_URL
from common import use_docker

simple_positive_json = {"bear_type": "BLACK",
                        "bear_name": "BOB",
                        "bear_age": 10.0}

bear_keys = ['bear_type', 'bear_name', 'bear_age', 'bear_id']

bear_types_positive = ['POLAR', 'BROWN', 'BLACK', 'GUMMY']
bear_names_positive = ['bob', 'BoB', 'B', 'b', 'a'*10]
bear_ages_positive = [0.1, 1, 50, 99, 100.0, 33.33333]

bear_types_negative = ['POLAr', 'brown', 'WHITE', '!,.[]', '']
bear_names_negative = [1, [], {1: 1}, 'a'*11, '']
bear_ages_negative = [-1, -1.0, 0.0, 101, 100.1, 'bob', [], {1: 1}, '']

bear_get_negative = [66666, 'a', {1: 1}, [0]]

headers = ['application/xml', 'application/zip', 'application/foobar']


@pytest.fixture(scope='class')
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


@pytest.fixture()
def clear():
    """clear data base before every test"""
    resp_del = requests.delete(REST_URL + '/bear')
    assert resp_del.status_code == 200


@pytest.mark.usefixtures('smoke_test','clear')
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
        assert isinstance(json_result['bear_name'], str)
        assert isinstance(json_result['bear_age'], float)
        assert isinstance(json_result['bear_id'], int)
        assert isinstance(json_result['bear_type'], str)

    def test_positive_id_incrementation_create_bear(self) -> None:
        """Check proper bear id incrementation"""

        bear_id_1 = requests.post(REST_URL + '/bear', json=simple_positive_json).json()
        bear_id_2 = requests.post(REST_URL + '/bear', json=simple_positive_json).json()

        assert bear_id_2 == bear_id_1 + 1

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

    def test_negative_create_bear_user_ids(self) -> None:
        """Negative bear POST create. Set id by client"""

        bear_id = 4242
        json = copy.copy(simple_positive_json)
        json.update({'bear_id': bear_id})

        resp_post = requests.post(REST_URL + '/bear', json=json)
        assert resp_post.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        assert resp_post.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        resp_get = requests.get(REST_URL + '/bear/{}'.format(bear_id))
        assert resp_get.text == 'EMPTY', 'TEXT: resp_get.text'.format(resp_get.text)

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
        """Positive check Delete One bear"""
        # create bear
        json_expected = copy.copy(simple_positive_json)
        bear_id = requests.post(REST_URL + '/bear', json=json_expected).json()

        # delete bear
        resp_del = requests.delete(REST_URL + '/bear/{}'.format(bear_id))
        assert resp_del.status_code == 200, 'STATUS CODE: {0}: {1}'.format(resp_del.status_code, resp_del.reason)
        resp_get = requests.get(REST_URL + '/bear/{}'.format(bear_id))
        assert resp_get.text == 'EMPTY', 'TEXT: resp_get.text'.format(resp_get.text)
        # How it should be:
        # assert resp_get.status_code == 404, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)

    def test_negative_delete_one_bear(self) -> None:
        """Negative check Delete One non-existent bear"""
        resp_del = requests.delete(REST_URL + '/bear/{}'.format(6666))
        assert resp_del.status_code == 404, 'STATUS CODE: {0}: {1}'.format(resp_del.status_code, resp_del.reason)

    def test_positive_get_all_delete_all_bears(self) -> None:
        """Positive check Get All + Delete All bears"""
        # create bears
        json_expected = copy.copy(simple_positive_json)
        for num in range(10):
            requests.post(REST_URL + '/bear', json=json_expected).json()

        # check get all bears
        resp_get = requests.get(REST_URL + '/bear')
        assert resp_get.status_code == 200, 'STATUS CODE: {0}: {1}'.format(resp_get.status_code, resp_get.reason)
        assert len(resp_get.json()) == 10

        # check delete all bears
        resp_del = requests.delete(REST_URL + '/bear')
        assert resp_del.status_code == 200, 'STATUS CODE: {0}: {1}'.format(resp_del.status_code, resp_del.reason)
        resp_get = requests.get(REST_URL + '/bear')
        assert resp_get.status_code == 200, 'STATUS CODE: {0}: {1}'.format(resp_get.status_code, resp_get.reason)
        assert len(resp_get.json()) == 0

    @pytest.mark.parametrize('bear_type', bear_types_positive, ids=bear_types_positive)
    @pytest.mark.parametrize('bear_name', bear_names_positive, ids=bear_names_positive)
    @pytest.mark.parametrize('bear_age', bear_ages_positive, ids=bear_ages_positive)
    def test_positive_update_specific_bear_all(self, bear_type: str, bear_name: str, bear_age: int or float) -> None:
        """Positive bear Update all items"""
        #  create simple bear
        requests.delete(REST_URL + '/bear')
        bear_id = requests.post(REST_URL + '/bear', json=simple_positive_json).json()
        json_expected = requests.get(REST_URL + '/bear/{}'.format(bear_id)).json()

        json_expected.update({'bear_type': bear_type, 'bear_name': bear_name.upper(), 'bear_age': float(bear_age)})
        update = {'bear_type': bear_type, 'bear_name': bear_name, 'bear_age': bear_age}
        resp_put = requests.put(REST_URL + '/bear/{}'.format(bear_id), json=update)

        assert resp_put.status_code == 200, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)
        json_result = requests.get(REST_URL + '/bear/{}'.format(bear_id)).json()
        assert json_result == json_expected

    @pytest.mark.parametrize('bear_type', bear_types_negative,
                             ids=lambda bear_types_negative: '{}'.format(bear_types_negative))
    def test_negative_update_specific_bear_type(self, bear_type) -> None:
        """Negative bear Update. WRONG bear_type"""
        #  create simple bear
        json = copy.copy(simple_positive_json)
        bear_id = requests.post(REST_URL + '/bear', json=simple_positive_json).json()
        json.update({'bear_id': bear_id})

        resp_put = requests.put(REST_URL + '/bear/{}'.format(bear_id), json={'bear_type': bear_type})

        assert json == requests.get(REST_URL + '/bear/{}'.format(bear_id)).json()
        assert resp_put.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)
        assert resp_put.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)

    @pytest.mark.parametrize('bear_name', bear_names_negative,
                             ids=lambda bear_names_negative: '{}'.format(bear_names_negative))
    def test_negative_update_specific_bear_name(self, bear_name) -> None:
        """Negative bear Update. WRONG bear_name"""
        #  create simple bear
        json = copy.copy(simple_positive_json)
        bear_id = requests.post(REST_URL + '/bear', json=simple_positive_json).json()
        json.update({'bear_id': bear_id})

        resp_put = requests.put(REST_URL + '/bear/{}'.format(bear_id), json={'bear_name': bear_name})

        assert json == requests.get(REST_URL + '/bear/{}'.format(bear_id)).json()
        assert resp_put.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)
        assert resp_put.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)

    @pytest.mark.parametrize('bear_age', bear_ages_negative,
                             ids=lambda bear_ages_negative: '{}'.format(bear_ages_negative))
    def test_negative_update_specific_bear_age(self, bear_age) -> None:
        """Negative bear Update. WRONG bear_age"""
        #  create simple bear
        json = copy.copy(simple_positive_json)
        bear_id = requests.post(REST_URL + '/bear', json=simple_positive_json).json()
        json.update({'bear_id': bear_id})

        resp_put = requests.put(REST_URL + '/bear/{}'.format(bear_id), json={'bear_age': bear_age})

        assert json == requests.get(REST_URL + '/bear/{}'.format(bear_id)).json()
        assert resp_put.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)
        assert resp_put.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)

    def test_negative_update_specific_bear_id(self) -> None:
        """Proof that there is no possibility to change bear_id by Update"""
        #create simple bear
        json = copy.copy(simple_positive_json)
        bear_id = requests.post(REST_URL + '/bear', json=simple_positive_json).json()
        json.update({'bear_id': bear_id})

        resp_put = requests.put(REST_URL + '/bear/{}'.format(bear_id), json={'bear_id': 666})

        assert json == requests.get(REST_URL + '/bear/{}'.format(bear_id)).json()
        assert resp_put.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)
        assert resp_put.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_put.status_code, resp_put.reason)

    @pytest.mark.parametrize('header', headers, ids=lambda headers: '{}'.format(headers))
    def test_negative_use_incorrect_header(self, header: str) -> None:
        """Negative http incorrect header check"""
        requests.delete(REST_URL + '/bear')
        resp_post = requests.post(REST_URL + '/bear', headers={"Content-type": header}, json=simple_positive_json)

        assert resp_post.text != 1
        assert resp_post.status_code != 200, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)
        assert resp_post.status_code == 400, 'STATUS CODE: {0}: {1}'.format(resp_post.status_code, resp_post.reason)

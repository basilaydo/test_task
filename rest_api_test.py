"""REST API Autotest"""
import requests
import pytest
import copy
import os
import sys
sys.path.append(os.getcwd())

from api import ApiClient, validate_response_code
from constants import DockerConstants, ApiConstants, HTTPCodes, Bears

# test data
SIMPLE_BEAR_JSON = {'bear_type': 'BLACK',
                    'bear_name': 'BOB',
                    'bear_age': 10.0}


bear_types_positive = ['POLAR', 'BROWN', 'BLACK', 'GUMMY']
bear_names_positive = ['bob', 'BoB', 'B', 'b', 'a'*10]
bear_ages_positive = [0.1, 1, 50, 99, 100.0, 33.33333]

bear_types_negative = ['POLAr', 'brown', 'WHITE', '!,.[]', '']
bear_names_negative = [1, [], {1: 1}, 'a'*11, '']
bear_ages_negative = [-1, -1.0, 0.0, 101, 100.1, 'bob', [], {1: 1}, '']

bear_get_negative = [66666, 'a', {1: 1}, [0]]

bear_id_negative = 666

database_size = 10

headers = ['application/xml', 'application/zip', 'application/foobar']


@pytest.fixture(scope='class')
def api_bear() -> ApiClient:
    """API fixture"""
    return ApiClient(base_url=DockerConstants.BASE_URL)


@pytest.fixture(scope='class')
def smoke_check(api_bear):
    """quick smoke check that checks basic functionality without which there is no sense to check test suit"""
    json_expected = copy.copy(SIMPLE_BEAR_JSON)

    # bear create check
    resp_post = api_bear.post_add(json=json_expected)
    validate_response_code(resp_post, HTTPCodes.OK)
    json_expected.update({'bear_id': resp_post.json()})

    # bear get check
    resp_get = api_bear.get_one(bear_id=resp_post.json())
    validate_response_code(resp_get, HTTPCodes.OK)
    json_result = resp_get.json()
    assert json_result == json_expected

    # all bears delete check
    resp_delete = api_bear.delete_all()
    validate_response_code(resp_delete, HTTPCodes.OK)
    assert not api_bear.get_all().json()


@pytest.fixture()
def clear(api_bear):
    """clear data base before every test"""
    resp_delete = api_bear.delete_all()
    validate_response_code(resp_delete, HTTPCodes.OK)


def create_simple_bear(api_bear) -> tuple:
    """create simple bear before test"""
    bear_id = api_bear.post_add(json=SIMPLE_BEAR_JSON).json()
    bear_json = copy.copy(SIMPLE_BEAR_JSON)
    bear_json.update({'bear_id': bear_id})
    return bear_id, bear_json


@pytest.mark.usefixtures('smoke_check', 'clear')
class TestAlaska:
    """Test suit for Alaska test"""

    @pytest.mark.parametrize('bear_type', bear_types_positive, ids=bear_types_positive)
    @pytest.mark.parametrize('bear_name', bear_names_positive, ids=bear_names_positive)
    @pytest.mark.parametrize('bear_age', bear_ages_positive, ids=bear_ages_positive)
    def test_positive_create_get_bear(self, api_bear, bear_type: str, bear_name: str, bear_age: int or float) -> None:
        """Positive bear POST create + GET read specific bear"""

        json_expected = {'bear_type': bear_type, 'bear_name': bear_name, 'bear_age': bear_age}
        resp_post = api_bear.post_add(json=json_expected)

        validate_response_code(resp_post, HTTPCodes.OK)
        json_expected.update({'bear_name': bear_name.upper(), 'bear_age': float(bear_age), 'bear_id': resp_post.json()})

        resp_get = api_bear.get_one(bear_id=resp_post.json())
        json_result = resp_get.json()
        assert json_result == json_expected
        assert isinstance(json_result['bear_name'], str), 'Incorrect bear_name type: {}'\
            .format(type(json_result['bear_name']))
        assert isinstance(json_result['bear_age'], float), 'Incorrect bear_age type: {}'\
            .format(type(json_result['bear_age']))
        assert isinstance(json_result['bear_id'], int), 'Incorrect bear_id type: {}'\
            .format(type(json_result['bear_id']))
        assert isinstance(json_result['bear_type'], str), 'Incorrect bear_type type: {}'\
            .format(type(json_result['bear_type']))

    def test_positive_bear_id_incrementation_create_bear(self, api_bear) -> None:
        """Check proper bear bear_id incrementation"""

        bear_id_1 = api_bear.post_add(json=SIMPLE_BEAR_JSON).json()
        bear_id_2 = api_bear.post_add(json=SIMPLE_BEAR_JSON).json()

        assert bear_id_2 == bear_id_1 + 1

    @pytest.mark.parametrize('bear_type', bear_types_negative,
                             ids=lambda bear_types_negative: '{}'.format(bear_types_negative))
    def test_negative_create_bear_types(self, api_bear, bear_type: str) -> None:
        """Negative bear POST create. WRONG bear_type"""

        json = copy.copy(SIMPLE_BEAR_JSON)
        json.update({'bear_type': bear_type})

        resp_post = api_bear.post_add(json=json)
        validate_response_code(resp_post, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_post, HTTPCodes.BAD_REQUEST)

    @pytest.mark.parametrize('bear_name', bear_names_negative,
                             ids=lambda bear_names_negative: '{}'.format(bear_names_negative))
    def test_negative_create_bear_names(self, api_bear, bear_name: str) -> None:
        """Negative bear POST create. WRONG bear_name"""

        json = copy.copy(SIMPLE_BEAR_JSON)
        json.update({'bear_name': bear_name})

        resp_post = api_bear.post_add(json=json)
        validate_response_code(resp_post, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_post, HTTPCodes.BAD_REQUEST)

    @pytest.mark.parametrize('bear_age', bear_ages_negative,
                             ids=lambda bear_ages_negative: '{}'.format(bear_ages_negative))
    def test_negative_create_bear_ages(self, api_bear, bear_age: int or float) -> None:
        """Negative bear POST create. WRONG bear_age"""

        json = copy.copy(SIMPLE_BEAR_JSON)
        json.update({'bear_age': bear_age})

        resp_post = api_bear.post_add(json=json)
        validate_response_code(resp_post, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_post, HTTPCodes.BAD_REQUEST)

    def test_negative_create_bear_user_ids(self, api_bear) -> None:
        """Negative bear POST create. Set bear_id by client"""

        bear_id = bear_id_negative
        json = copy.copy(SIMPLE_BEAR_JSON)
        json.update({'bear_id': bear_id})

        resp_post = api_bear.post_add(json=json)
        validate_response_code(resp_post, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_post, HTTPCodes.BAD_REQUEST)
        resp_get = api_bear.get_one(bear_id=bear_id)
        assert resp_get.text == Bears.GET_ALL_EMPTY_RESPONSE, 'TEXT: {}'.format(resp_get.text)

    @pytest.mark.parametrize('bear_id', bear_get_negative,
                             ids=lambda bear_get_negative: '{}'.format(bear_get_negative))
    def test_negative_get_bear(self, api_bear, bear_id) -> None:
        """Negative SPECIFIC bear GET read """

        resp_post = api_bear.get_one(bear_id=bear_id)
        if isinstance(bear_id, int):
            validate_response_code(resp_post, HTTPCodes.NOT_FOUND)
        else:
            validate_response_code(resp_post, HTTPCodes.BAD_REQUEST)

    def test_positive_delete_one_bear(self, api_bear) -> None:
        """Positive check Delete One bear"""
        # create bear
        json_expected = copy.copy(SIMPLE_BEAR_JSON)
        bear_id = api_bear.post_add(json=json_expected).json()

        # delete bear
        resp_delete = api_bear.delete(bear_id=bear_id)
        validate_response_code(resp_delete, HTTPCodes.OK)
        resp_get = api_bear.get_one(bear_id=bear_id)
        assert resp_get.text == Bears.GET_ALL_EMPTY_RESPONSE, 'TEXT: {}'.format(resp_get.text)
        # How it should be:
        # assert resp_get.status_code == 404

    def test_negative_delete_one_bear(self, api_bear) -> None:
        """Negative check Delete One non-existent bear"""
        resp_delete = api_bear.delete(bear_id=bear_id_negative)
        validate_response_code(resp_delete, HTTPCodes.NOT_FOUND)

    def test_positive_get_all_delete_all_bears(self, api_bear) -> None:
        """Positive check Get All + Delete All bears"""
        # create bears
        json_expected = copy.copy(SIMPLE_BEAR_JSON)
        for num in range(database_size):
            api_bear.post_add(json=json_expected).json()

        # check get all bears
        resp_get = api_bear.get_all()
        validate_response_code(resp_get, HTTPCodes.OK)
        assert len(resp_get.json()) == database_size

        # check delete all bears
        resp_delete = api_bear.delete_all()
        validate_response_code(resp_delete, HTTPCodes.OK)
        resp_get = api_bear.get_all()
        validate_response_code(resp_get, HTTPCodes.OK)
        assert len(resp_get.json()) == 0

    @pytest.mark.parametrize('bear_type', bear_types_positive, ids=bear_types_positive)
    @pytest.mark.parametrize('bear_name', bear_names_positive, ids=bear_names_positive)
    @pytest.mark.parametrize('bear_age', bear_ages_positive, ids=bear_ages_positive)
    def test_positive_update_specific_bear_all(self, api_bear, bear_type: str, bear_name: str,
                                               bear_age: int or float) -> None:
        """Positive bear Update all items"""
        bear_id, json_expected = create_simple_bear(api_bear)

        json_expected.update({'bear_type': bear_type, 'bear_name': bear_name.upper(), 'bear_age': float(bear_age)})
        update = {'bear_type': bear_type, 'bear_name': bear_name, 'bear_age': bear_age}
        resp_put = api_bear.put_one(bear_id=bear_id, json=update)

        validate_response_code(resp_put, HTTPCodes.OK)
        json_result = api_bear.get_one(bear_id=bear_id).json()
        assert json_result == json_expected

    @pytest.mark.parametrize('bear_type', bear_types_negative,
                             ids=lambda bear_types_negative: '{}'.format(bear_types_negative))
    def test_negative_update_specific_bear_type(self, api_bear, bear_type) -> None:
        """Negative bear Update. WRONG bear_type"""
        bear_id, json_expected = create_simple_bear(api_bear)

        resp_put = api_bear.put_one(bear_id=bear_id, json={'bear_type': bear_type})

        assert json_expected == api_bear.get_one(bear_id=bear_id).json()
        validate_response_code(resp_put, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_put, HTTPCodes.BAD_REQUEST)

    @pytest.mark.parametrize('bear_name', bear_names_negative,
                             ids=lambda bear_names_negative: '{}'.format(bear_names_negative))
    def test_negative_update_specific_bear_name(self, api_bear, bear_name) -> None:
        """Negative bear Update. WRONG bear_name"""
        bear_id, json_expected = create_simple_bear(api_bear)

        resp_put = api_bear.put_one(bear_id=bear_id, json={'bear_name': bear_name})

        assert json_expected == api_bear.get_one(bear_id=bear_id).json()
        validate_response_code(resp_put, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_put, HTTPCodes.BAD_REQUEST)

    @pytest.mark.parametrize('bear_age', bear_ages_negative,
                             ids=lambda bear_ages_negative: '{}'.format(bear_ages_negative))
    def test_negative_update_specific_bear_age(self, api_bear, bear_age) -> None:
        """Negative bear Update. WRONG bear_age"""
        bear_id, json_expected = create_simple_bear(api_bear)

        resp_put = api_bear.put_one(bear_id=bear_id, json={'bear_age': bear_age})

        assert json_expected == api_bear.get_one(bear_id=bear_id).json()
        validate_response_code(resp_put, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_put, HTTPCodes.BAD_REQUEST)

    def test_negative_update_specific_bear_id(self, api_bear) -> None:
        """Proof that there is no possibility to change bear_id by Update"""
        bear_id, json_expected = create_simple_bear(api_bear)
        print(bear_id)
        print(json_expected)
        resp_put = api_bear.put_one(bear_id=bear_id, json={'bear_id': bear_id_negative})

        assert json_expected == api_bear.get_one(bear_id=bear_id).json()
        validate_response_code(resp_put, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_put, HTTPCodes.BAD_REQUEST)

    @pytest.mark.parametrize('header', headers, ids=lambda headers: '{}'.format(headers))
    def test_negative_use_incorrect_header(self, api_bear, header: str) -> None:
        """Negative http incorrect header check"""
        api_bear.delete_all()
        resp_post = api_bear.post_add(headers={"Content-type": header}, json=SIMPLE_BEAR_JSON)

        assert resp_post.text != 1
        validate_response_code(resp_post, HTTPCodes.OK, should_be_equal=False)
        validate_response_code(resp_post, HTTPCodes.BAD_REQUEST)

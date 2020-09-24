"""Common constants"""


class DockerConstants:
    """Docker constants"""
    DOCKER_IMAGE = 'azshoo/alaska'
    DOCKER_TAG = 'latest'
    HOST = '0.0.0.0'
    PORT = 8091
    CONNECT_TIMEOUT = 60
    BASE_URL = "http://{0}:{1}".format(HOST, PORT)


class ApiConstants:
    """API constants"""
    POST_ADD_PATH = '/bear'
    GET_INFO_PATH = '/info'
    GET_ONE_PATH = '/bear/'
    GET_ALL_PATH = '/bear'
    PUT_ONE_PATH = '/bear/'
    DELETE_ONE_PATH = '/bear/'
    DELETE_ALL_PATH = '/bear'


class Bears:
    """Bear constants"""
    GET_ALL_EMPTY_RESPONSE = 'EMPTY'


class HTTPCodes:
    """HTTP response codes"""
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

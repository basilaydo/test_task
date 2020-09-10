import docker
import time
import requests
from socket import create_connection
import pytest

DOCKER_IMAGE = 'azshoo/alaska'
DOCKER_TAG = 'latest'

HOST = '0.0.0.0'
PORT = 8091

REST_URL = "http://{0}:{1}".format(HOST, PORT)


@pytest.fixture(scope='session', autouse=True)
def use_docker(image=DOCKER_IMAGE, tag=DOCKER_TAG, host=HOST, port=PORT, timeout=60):
    """Fixture that runs docker container on start and stops upon completion a session

    :param image: docker image
    :type image: str
    :param tag: docker tag
    :type tag: str
    :param host: host IP
    :type host: str
    :param port: TCP port
    :type port: int
    :param timeout: connection timeout
    :type timeout: int
    :return: None
    """
    run_kwargs = {
        "image": "{0}:{1}".format(image, tag),
        "detach": True,
        "tty": True,
        "ports": {port: port},
    }

    client = docker.from_env()
    container = client.containers.run(**run_kwargs)

    start_time = time.perf_counter()
    while True:
        try:
            with create_connection((host, port), timeout=timeout):
                response = requests.get("http://{0}:{1}/info".format(host, port))
                if response.status_code == 200:
                    break
        except (OSError, ConnectionResetError) as ex:
            time.sleep(0.1)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError('Waited too long for the http://{0}:{1} to start accepting connections.'
                                   .format(host, port))

    yield

    container.stop()
    container.remove()

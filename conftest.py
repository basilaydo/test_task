"""Fixtures for tests"""

import os
import sys
sys.path.append(os.getcwd())

import docker
import time
import requests
from socket import create_connection
from constants import DockerConstants
import pytest
from logger import set_common_logger, create_test_logger


@pytest.fixture(scope='session', autouse=False)
def use_docker(image=DockerConstants.DOCKER_IMAGE, tag=DockerConstants.DOCKER_TAG, host=DockerConstants.HOST,
               port=DockerConstants.PORT, timeout=DockerConstants.CONNECT_TIMEOUT):
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


def pytest_configure():
    # Set console log level for a project
    console_log_lvl = os.getenv('CONSOLE_LOG_LEVEL', 'INFO')
    set_common_logger(console_level=console_log_lvl)


@pytest.fixture(autouse=True)
def logger(request):
    """Instance of test logger which will be created for each test"""
    yield create_test_logger(request.node.name)

import pytest
import allure
import copy
import os
import sys
from logger import create_test_logger

logger = create_test_logger('LoL_class')

class LoL:
    def __init__(self):
        self.a = 3
        logger.info('LOOOL')


@pytest.fixture()
def init_lol():
    return LoL()


@allure.feature('Test Suite to test features')
class TestTest:

    @allure.feature('test for test')
    def test_test(self, logger, init_lol):

        lol = init_lol

        logger.info(f'lol object {lol}')
        logger.info('my_info')
        logger.warning('my_warning')
        logger.critical('my_critical')
        logger.debug('my_debug')
        with allure.step('step'):

            assert 1 == 1

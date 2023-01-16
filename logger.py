"""Logger tools"""

import sys
import loguru

COMMON_LOG_FORMAT = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {extra[name]}\n\t{module}: {message}'
TEST_LOG_FORMAT = "<level>{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}/{function} | <c>{message}</c></level>"


def set_common_logger(console_level: str):
    loguru.logger.remove()
    loguru.logger.add(sys.stdout, level=console_level, enqueue=True, format=TEST_LOG_FORMAT)
    loguru.logger.add('reports/full_tests.log', level='DEBUG', enqueue=True, format=COMMON_LOG_FORMAT)


def create_test_logger(test_name: str):
    test_logger = loguru.logger.bind(name=test_name)
    test_log_path = f'reports/logs/{test_name.replace("/", "_")}.log'
    test_logger.add(test_log_path, format=TEST_LOG_FORMAT,
                    filter=lambda record: record["extra"].get("name") == test_name)
    test_logger.info(f'Start test: {test_name}')
    return test_logger

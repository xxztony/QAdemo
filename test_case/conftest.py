import time
from pathlib import Path

import pytest
import uiautomator2 as u2

from common.automation_config import AutomationConfig
from common.custom_logger import CustomLogger
from page.android.home_page import HomePage
from page.android.nine_day_page import NineDayPage

images_path = Path(__file__).parents[1] / 'image'


@pytest.fixture(autouse=True)
def print_start_and_end(request):
    CustomLogger.print_with_new_line(f"---------- Start test {request.node.name}---------------")
    yield
    CustomLogger.print_with_new_line(f"---------- End test {request.node.name}---------------")


@pytest.fixture(scope="class")
def driver(automation_config):
    """
    uiautomator2 driver
    :return:
    """
    driver = u2.connect_usb(automation_config.get('serial_no'))
    CustomLogger.print_log(driver.device_info)
    CustomLogger.print_log('Open MyObservatory APP')
    driver.app_start('hko.MyObservatory_v1_0', wait=True)
    time.sleep(10)
    yield driver
    CustomLogger.print_log('close APP')
    driver.app_stop('hko.MyObservatory_v1_0')


@pytest.fixture(scope="class")
def home_page(driver):
    """
    init quote page; remove all securities in watchlist before/after test
    :return:
    """
    home_page = HomePage(driver)
    return home_page


@pytest.fixture(scope="function")
def nine_day_page(home_page):
    """
    init quote page; remove all securities in watchlist before/after test
    :return:
    """
    nine_day_page = NineDayPage(home_page)
    # nine_day_page.go_to_nine_page()
    # nine_day_temp,nine_day_rh,nine_day_date,nine_day_week_date,nine_day_psr = nine_day_page.get_nine_day_weather_day_info()
    # update_date = nine_day_page.get_update_date()
    yield nine_day_page
    time.sleep(2)


@pytest.fixture(scope='session')
def automation_config():
    """
    init test config
    :return:
    """
    return AutomationConfig().config


def pytest_html_report_title(report):
    """
    change html_report title
    :param report:
    :return:
    """
    report.title = "自动化测试报告"

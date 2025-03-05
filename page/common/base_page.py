import os
import time
from datetime import datetime
from pathlib import Path

import aircv as ac

from common.custom_logger import CustomLogger
from common.locate_type import LocateBy


class BasePage:
    """
    基础页面类，包含常用的Appium操作方法，支持Android和iOS
    """

    def __init__(self, driver):
        self.driver = driver
        self.operation_count = 0

    def start_app(self, package, wait=True):
        """
        start app
        :param package: package code to start
        :param wait: if wait app start
        :return:
        """
        self.driver.app_start(package, wait=wait)

    def stop_app(self, package):
        """
        stop app
        :param package: package code to stop
        :return:
        """
        self.driver.app_stop(package)

    def click_home(self):
        """
        click home button
        :return:
        """
        self.driver.press("home")

    def find_element_by_xpath(self, xpath, timeout=5):
        """
        通过xpath定位元素
        :param xpath: xpath表达式
        :return: 元素对象
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                return self.driver.driver.xpath(xpath)
            except Exception:
                time.sleep(0.1)  # 每次重试间隔0.1秒
        # 超时后抛出异常
        raise Exception(f"在 {timeout} 秒内通过xpath定位元素失败: {xpath}")

    def find_element_by_id(self, resource_id, timeout=5):
        """
        通过id定位元素（Android使用resource-id，iOS使用accessibility id）
        :param resource_id: 元素id
        :param timeout: 超时时间
        :return: 元素对象
        """
        try:
            # Android使用resource-id
            element = self.driver.find_element_by_id(resource_id)
            if not element:
                # iOS尝试使用accessibility id
                element = self.driver.find_element_by_accessibility_id(resource_id)
            return element
        except Exception as e:
            CustomLogger.print_log(f"通过id定位元素失败: {e}")
            return None

    def find_element_by_text(self, class_name, text, index, timeout=5):
        """
        get element class name and text
        :param class_name: class name of element
        :param text: element text
        :param index: index
        :return: element
        """
        self.driver(className=class_name, text=text).wait(timeout=timeout)
        return self.driver(className=class_name, text=text)[index]

    def find_element_by_text_contains(self, class_name, text_contains, index, timeout=5):
        """
        get element class name and contains text
        :param class_name: class name of element
        :param text_contains: matched text
        :param index: index
        :return: element
        """
        self.driver(className=class_name, textContains=text_contains).wait(timeout=timeout)
        return self.driver(className=class_name, textContains=text_contains)[index]

    def find_element(self, locator, timeout=5):
        """
        统一的元素定位方法
        :param locator: 定位器字典，格式为 {定位方式: 定位值}
        :param timeout: 超时时间
        :return: 元素对象
        """
        (locate_method, locate_value), = locator.items()
        try:
            if locate_method == LocateBy.ID.value:
                element = self.find_element_by_id(locate_value, timeout)
            elif locate_method == LocateBy.XPATH.value:
                element = self.find_element_by_xpath(locate_value, timeout)
            elif locate_method == LocateBy.IOS_PREDICATE.value:
                element = self.driver.find_element_by_ios_predicate(locate_value)
            elif locate_method == LocateBy.IOS_CLASS_CHAIN.value:
                element = self.driver.find_element_by_ios_class_chain(locate_value)
            elif locate_method == LocateBy.ACCESSIBILITY_ID.value:
                element = self.driver.find_element_by_accessibility_id(locate_value)
            elif locate_method == LocateBy.TEXT.value:
                element = self.find_element_by_text(locate_value[0], locate_value[1], 0, timeout)
            elif locate_method == LocateBy.TEXT_CONTAINS.value:
                element = self.find_element_by_text_contains(locate_value[0], locate_value[1], 0, timeout)
            else:
                raise Exception("不支持的定位方法")

            return element
        except Exception as e:
            CustomLogger.print_log(f"元素定位失败: {e}")
            return None

    def click(self, locator):
        """
        点击元素
        :param locator: 定位器字典
        """
        element = self.find_element(locator)
        if element:
            self.operation_count_print()
            CustomLogger.print_log('正在点击元素')
            element.click()

    def long_click(self, locator, duration=3):
        """
        long click element
        :param locator: locator dict
        :param duration: long click duration
        :return:
        """
        element = self.find_element(locator)
        if element:
            self.operation_count_print()
            CustomLogger.print_log(f'正在进行元素长按')
            element.long_click(duration)

    def swipe_by_screen(self, direction):
        """
        swipe screen
        :param direction: direction，including ['left', 'right', 'up', 'down']
        :return:
        """
        if direction not in ['left', 'right', 'up', 'down']:
            raise Exception("Error direction, please input on of 'left', 'right', 'up', 'down'")
        self.operation_count_print()
        self.driver.swipe_ext(direction)

    def send_keys(self, locator, text):
        """
        输入文本
        :param locator: 定位器字典
        :param text: 要输入的文本
        """
        element = self.find_element(locator)
        if element:
            self.operation_count_print()
            CustomLogger.print_log(f'输入文本: {text}')
            element.clear()
            element.send_keys(text)

    def clear_text(self, locator, index=0):
        """
        clear text
        :param locator: locator dict
        :param index: index
        :return:
        """
        element = self.find_element(locator, index)
        if element:
            self.operation_count_print()
            element.clear_text()

    def get_text(self, locator, index=0):
        """
        get element text
        :param locator: locator dict
        :param index: index
        :return: element text
        """
        element = self.find_element(locator, index)
        if element:
            self.operation_count_print()
            element.get_text()

    def element_screenshot(self, locator=None, index=0) -> Path:
        """
        get screenshot
        :param locator: locator dict
        :param index: index
        :return: image filepath
        """
        image_path = Path(__file__).parents[1]
        pic_time = datetime.now().strftime("%Y%m%d%H%M%S")
        screen_image_name = image_path / 'image' / ("screen_img_" + pic_time + ".png")
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        self.operation_count_print()
        CustomLogger.print_log(f'截图并保存到{screen_image_name}')
        if locator:
            self.find_element(locator, index).screenshot().save(screen_image_name)
        else:
            self.driver.screenshot().save(screen_image_name)
        return screen_image_name

    def is_exist(self, locator, timeout=1):
        """
        if element exists
        :param locator: locator dict
        :param timeout: timeout(s)
        :param index: index
        :return: if element exists
        """
        (locate_method, locate_value), = locator.items()
        if locate_method == LocateBy.ID.value:
            return self.driver(resourceId=locate_value).wait(timeout=timeout)
        elif locate_method == LocateBy.XPATH.value:
            a = self.driver.xpath(locate_value).wait(timeout=timeout)
            return True if self.driver.xpath(locate_value).wait(timeout=timeout) else False
        elif locate_method == LocateBy.TEXT.value:
            return self.driver(className=locate_value[0], text=locate_value[1]).wait(timeout=timeout)
        elif locate_method == LocateBy.TEXT_CONTAINS.value:
            return self.driver(className=locate_value[0], textContains=locate_value[1]).wait(timeout=timeout)
        else:
            raise Exception("locate method not supported")

    def click_image(self, image_name=None, threshold=0.9):
        """
        click image based on aircv
        :param image_name: target image to identify
        :param threshold: threshold to identify
        :return: str
        """
        target_img = ac.imread(image_name)
        for i in range(2):
            # current screen
            screen_image = self.driver.screenshot(format='opencv')
            position = ac.find_template(screen_image, target_img, threshold)
            if position and 'result' in position:
                x, y = position['result']
                self.operation_count_print()
                self.driver.click(x, y)
                self.operation_count_print()
                CustomLogger.print_log("点击了目标图像")
                return x, y
            else:
                CustomLogger.print_log("未找到目标图像")
                time.sleep(1)

    def operation_count_print(self):
        """
        get operation count
        :return:
        """
        self.operation_count += 1
        CustomLogger.print_log(f'正在进行第{self.operation_count}次元素点击|输入|信息获取')

    def reset_operation_count(self):
        CustomLogger.print_debug(f'重置操作计数')
        self.operation_count += 0

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
        滑动操作
        :param start_x: 起始x坐标
        :param start_y: 起始y坐标
        :param end_x: 结束x坐标
        :param end_y: 结束y坐标
        :param duration: 持续时间（毫秒）
        """
        self.operation_count_print()
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

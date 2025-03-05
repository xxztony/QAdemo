from collections import abc
from pathlib import Path

import yaml

from common.custom_logger import CustomLogger


class AutomationConfig:
    """
    自动化测试配置管理类
    
    该类负责管理自动化测试的配置信息，按以下顺序读取配置：
    1. 读取基础配置
    2. 读取测试环境配置并从系统环境变量覆盖
    3. 读取测试环境配置文件
    4. 读取覆盖配置文件
    
    属性:
        my_automation_environment_config_file (str): 本地配置文件名
        config (dict): 存储所有配置信息的字典
        config_dir (Path): 配置文件目录路径
        config_file_path (Path): 配置文件完整路径
    """

    my_automation_environment_config_file = 'automation_local.yaml'

    def __init__(self):
        """
        初始化配置管理器
        
        设置基础配置路径并加载配置文件
        """
        self.config = dict()
        self.my_environment = None
        base_dir = Path(__file__).parents[1]
        self.config_dir = base_dir / 'test_environment_config'
        self.config_file_path = self.config_dir / self.my_automation_environment_config_file
        self.configure_automation()

    def configure_automation(self):
        """
        加载自动化测试配置
        
        从配置文件中读取配置信息，并更新到config字典中。
        如果配置文件不存在或读取失败，会记录相应的调试信息。
        """
        # 加载默认配置文件
        CustomLogger.print_debug('\n开始扫描自动化配置文件目录')
        self.debugIsConfigFileFound = Path(self.config_file_path).exists()
        self.debugFileFoundStr = '找到配置文件' if self.debugIsConfigFileFound else '未找到配置文件'
        CustomLogger.print_debug('基础目录为: {}'.format(self.config_dir))
        with open(self.config_file_path) as my_config:
            # 加载基础配置
            temp_config = yaml.safe_load(my_config)
            self.config.update(temp_config)


def update(source_config: dict, update_file: dict) -> dict:
    """
    update test config file
    :param source_config: the input dict that need to be updated
    :param update_file: the dict used to update source_config
    :return:
    """
    for key, value in update_file.items():
        if isinstance(value, abc.Mapping):
            source_config[key] = update(source_config.get(key, {}), value)
        else:
            source_config[key] = value
    return source_config

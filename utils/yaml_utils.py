#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:10
# @Author  : 地核桃
# @file: yaml_utils.py
# @desc:


import yaml
from pathlib import Path

import yaml
from pathlib import Path
from utils.path_utils import get_project_root

class YamlUtils:
    @staticmethod
    def load_yaml(rel_path):
        """通用加载方法，传入相对于项目根目录的路径"""
        root = get_project_root()
        full_path = root / rel_path
        with open(full_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_data(file_name):
        """专门加载 data 目录下的数据"""
        return YamlUtils.load_yaml(f"data/{file_name}")

    @staticmethod
    def load_locator(file_name):
        """专门加载 locators 目录下的文件"""
        return YamlUtils.load_yaml(f"locators/{file_name}")
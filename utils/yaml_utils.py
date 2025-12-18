#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:10
# @Author  : 地核桃
# @file: yaml_utils.py
# @desc:

import yaml
from utils.path_utils import get_project_root

class YamlUtils:
    @staticmethod
    def load_yaml(rel_path):
        root = get_project_root()
        full_path = root / rel_path
        with open(full_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_data(file_name):
        """加载 data 目录下的数据"""
        return YamlUtils.load_yaml(f"data/{file_name}")

    @staticmethod
    def load_locator(file_name):
        """加载 locators 目录下的文件"""
        return YamlUtils.load_yaml(f"locators/{file_name}")
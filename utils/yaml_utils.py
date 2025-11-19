#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:10
# @Author  : 地核桃
# @file: yaml_utils.py
# @desc:


import yaml
from pathlib import Path

class YamlUtils:
    @staticmethod
    def load_yaml(file_path):
        full_path = Path(file_path).resolve()  # 转换为绝对路径
        print(f"程序实际查找的配置文件路径：{full_path}")  # 新增打印
        with open(full_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
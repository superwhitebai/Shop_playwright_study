#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 22:11
# @Author  : 地核桃
# @file: path_utils.py.py
# @desc:

from pathlib import Path

def get_project_root():
    """获取项目根目录"""
    current_file = Path(__file__).resolve()
    return current_file.parent.parent
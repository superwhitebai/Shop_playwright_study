#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/19 00:41
# @Author  : 地核桃
# @file: conftest.py.py
# @desc:

import sys
from pathlib import Path

# 获取 conftest.py
current_dir = Path(__file__).resolve().parent
print(f"当前 conftest.py 所在目录：{current_dir}")  # 打印确认

sys.path.append(str(current_dir))
print(f"添加到 sys.path 的路径：{current_dir}")  # 打印出所在
print(f"当前 sys.path 列表：{sys.path}")  # 查看是否包含目标路径


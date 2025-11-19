#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:24
# @Author  : 地核桃
# @file: conftest.py.py
# @desc:
import pytest
from playwright.sync_api import sync_playwright
from utils.yaml_utils import YamlUtils

@pytest.fixture(scope="session")
def config():
    """加载全局配置"""
    return YamlUtils.load_yaml("config/config.yaml")

@pytest.fixture(scope="function")
def page():
    """创建Playwright页面对象，自动关闭"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 非无头模式，可看到浏览器操作
        page = browser.new_page()
        yield page
        page.close()
        browser.close()
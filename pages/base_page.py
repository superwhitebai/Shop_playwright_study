#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:11
# @Author  : 地核桃
# @file: base_page.py
# @desc:

from playwright.sync_api import Page
from utils.yaml_utils import YamlUtils
import allure
from playwright.sync_api import Page

import allure

class BasePage:
    def __init__(self, page):
        self.page = page
        self.locators = {}

    def load_locators(self, locator_file):
        """加载元素定位文件"""
        self.locators = YamlUtils.load_yaml(f"config/{locator_file}")
        return self

    @allure.step("打开网址: {url}")
    def goto(self, url: str):
        """打开指定网址并等待加载完成"""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    @allure.step("点击元素: {locator}")
    def click(self, locator: str):
        """点击指定定位的元素"""
        self.page.locator(locator).click()

    def input_text(self, locator, text):
        """封装输入文本的通用方法"""
        self.page.locator(locator).fill(text)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from playwright.sync_api import Page
from utils.yaml_utils import YamlUtils
import allure

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = {}

    def load_locators(self, locator_file_name):
        """
        加载 locators 目录下的 yaml 文件
        :param locator_file_name: 例如 'login_page.yaml'
        """
        # 这里的 load_locator 会自动处理 locators/ 前缀
        self.locators = YamlUtils.load_locator(locator_file_name)
        return self

    @allure.step("打开网址: {url}")
    def goto(self, url: str):
        """打开指定网址并等待加载完成"""
        self.page.goto(url)
        # 等待网络空闲，确保页面完全加载
        self.page.wait_for_load_state("networkidle")

    @allure.step("点击元素")
    def click(self, locator: str):
        """点击指定定位的元素"""
        # 这里的 locator 是具体的定位符字符串
        self.page.locator(locator).click()

    @allure.step("输入文本: {text}")
    def input_text(self, locator: str, text: str):
        """封装输入文本的通用方法"""
        self.page.locator(locator).fill(text)
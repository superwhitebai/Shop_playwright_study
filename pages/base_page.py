#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 17:11
# @Author  : 地核桃
# @file: base_page.py
# @desc:
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from playwright.sync_api import Page, Locator
import allure
from utils.yaml_utils import YamlUtils
from utils.logger_utils import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = {}
        self.logger = get_logger(self.__class__.__name__)

    def load_locators(self, locator_file_name):
        """
        加载 locators 目录下的 yaml 文件
        """
        self.locators = YamlUtils.load_locator(locator_file_name)
        return self

    @allure.step("打开网址: {url}")
    def goto(self, url: str):
        self.logger.info(f"正在访问网址: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    @allure.step("点击元素")
    def click(self, locator: str):

        self.logger.info(f"点击元素: {locator}")
        self.page.locator(locator).click()

    @allure.step("输入文本: {text}")
    def input_text(self, locator: str, text: str):
        self.logger.info(f"向元素 [{locator}] 输入文本: {text}")
        self.page.locator(locator).fill(text)

    def log(self, message):
        self.logger.info(message)
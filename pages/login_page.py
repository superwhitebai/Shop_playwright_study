#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:15
# @Author  : 地核桃
# @file: login_page.py.py
# @desc:
import allure

from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.load_locators("locators/login_locators.yaml")
        # 从定位器字典中提取登录按钮的定位表达式，赋值给属性
        self.login_button_locator = self.locators["login_button"]["locator"]

    @allure.step("点击登录按钮")
    def click_login_button(self):
        self.click(self.login_button_locator)
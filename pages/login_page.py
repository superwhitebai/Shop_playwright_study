#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:15
# @Author  : 地核桃
# @file: login_page.py.py
# @desc:
import allure

from pages.base_page import BasePage

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
from pages.base_page import BasePage

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # 加载 yaml 定位文件
        self.load_locators("login_page.yaml")

        # 初始化属性（从 yaml 中读取）
        self.login_input_locator = self.locators["login_input"]["locator"]
        self.password_input_locator = self.locators["password_input"]["locator"]
        self.form_login_button_locator = self.locators["form_login_button"]["locator"]
        self.toast_message_locator = self.locators["toast_message_locator"]["locator"]

        self.logout_button_locator = self.locators.get("logout_button", {}).get("locator")

    @allure.step("点击登录按钮（进入登录页）")
    def click_login_button(self):
        self.click(self.locators["login_button"]["locator"])

    @allure.step("输入登录账号")
    def input_login_input(self, username):
        self.input_text(self.login_input_locator, username)

    @allure.step("输入登录密码")
    def input_password_input(self, password):
        self.input_text(self.password_input_locator, password)

    @allure.step("点击表单内的登录提交按钮")
    def click_form_login_button(self):
        locator = self.page.locator(self.form_login_button_locator)
        locator.wait_for(state="visible", timeout=10000)
        locator.click()

    @allure.step("获取页面错误提示文本")
    def get_error_message(self):
        toast_locator = self.page.locator(self.toast_message_locator)
        toast_locator.wait_for(state="visible", timeout=5000)
        return toast_locator.text_content().strip()

    @allure.step("点击退出登录")
    def click_logout(self):
        if not self.logout_button_locator:
            raise ValueError("Yaml中缺少 logout_button 定位符，请检查 locators/login_page.yaml")
        self.page.locator(self.logout_button_locator).wait_for(state="visible")
        self.click(self.logout_button_locator)
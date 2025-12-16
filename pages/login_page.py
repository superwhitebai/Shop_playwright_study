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


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.load_locators("login_page.yaml")

        # 初始化属性
        self.login_input_locator = self.locators["login_input"]["locator"]
        self.password_input_locator = self.locators["password_input"]["locator"]
        self.form_login_button_locator = self.locators["form_login_button"]["locator"]
        self.toast_message_locator = self.locators["toast_message_locator"]["locator"]
        self.login_button_locator = self.locators["login_button"]["locator"]

    @allure.step("点击登录按钮")
    def click_login_button(self):
        self.click(self.login_button_locator)

    @allure.step("输入登录账号")
    def input_login_input(self, username):
        self.input_text(self.login_input_locator, username)

    @allure.step("输入登录密码")
    def input_password_input(self, password):
        self.input_text(self.password_input_locator, password)

    @allure.step("点击表单内的登录提交按钮")
    def click_form_login_button(self):
        locator = self.page.locator(self.form_login_button_locator)
        # 这里的 visible=true 已经在 yaml 里处理了，这里直接等待即可
        locator.wait_for(state="visible", timeout=10000)
        locator.click()

    @allure.step("捕获密码错误Toast")
    def get_password_error_toast(self):
        toast_locator = self.page.locator(self.toast_message_locator)
        toast_locator.wait_for(state="visible", timeout=10000)
        # 返回Toast文本
        return toast_locator.text_content().strip()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/24 19:23
# @Author  : 地核桃
# @file: register_page.py.py
# @desc:
import allure
from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.load_locators("register_page.yaml")

        self.enter_register_link_loc = self.locators["enter_register_link"]["locator"]
        self.username_input_loc = self.locators["username_input"]["locator"]
        self.password_input_loc = self.locators["password_input"]["locator"]
        self.register_button_loc = self.locators["register_button"]["locator"]
        self.prompt_message_loc = self.locators["prompt_message"]["locator"]

    @allure.step("点击首页注册链接")
    def click_enter_register(self):
        self.click(self.enter_register_link_loc)

    @allure.step("输入注册用户名: {username}")
    def input_username(self, username):
        self.input_text(self.username_input_loc, username)

    @allure.step("输入注册密码")
    def input_password(self, password):
        self.input_text(self.password_input_loc, password)

    @allure.step("点击注册按钮")
    def click_register_submit(self):
        self.click(self.register_button_loc)

    @allure.step("获取提示信息")
    def get_prompt_message(self):
        return self.page.locator(self.prompt_message_loc).wait_for(state="visible").text_content()

    @allure.step("获取注册成功提示")
    def get_success_message(self):
        return self.page.locator(self.register_success_loc).wait_for(state="visible", timeout=10000).text_content()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:25
# @Author  : 地核桃
# @file: test_login.py.py
# @desc:

import allure
import pytest
from pages.login_page import LoginPage


@allure.feature("ShopXO 登录流程")
class TestLogin:  # 类名以 Test 开头，Pytest 会自动识别
    def test_open_url_and_click_login(self, page, config):
        # 初始化登录页对象
        login_page = LoginPage(page)

        # 打开ShopXO官网
        login_page.goto(config["base_url"])

        # 点击登录按钮
        login_page.click_login_button()

        # 简单断言：验证是否跳转到登录相关页面（可根据实际URL调整）
        assert "login" in page.url.lower()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:25
# @Author  : 地核桃
# @file: test_login.py.py
# @desc:
import time
import allure
from pages.login_page import LoginPage
from utils.yaml_utils import YamlUtils


@allure.feature("ShopXO 登录流程")
class TestLogin:
    def test_open_url_and_click_login(self, page, config):
        login_page = LoginPage(page)
        login_page.goto(config["base_url"])
        login_page.click_login_button()
        account = YamlUtils.get_account()

        # 输入账号 + 错误密码（触发Toast）
        login_page.input_login_input(account["username"])
        login_page.input_password_input(account["password"])  # 错误密码

        # 调试打印
        print("当前登录按钮定位符：", login_page.form_login_button_locator)
        print("匹配元素数量：", page.locator(login_page.form_login_button_locator).count())

        # 点击登录提交
        login_page.click_form_login_button()

        # 捕获Toast
        toast_text = login_page.get_password_error_toast()
        print(f"密码错误时的Toast：{toast_text}")

        # 🌟 显性断言（带明确提示）
        expected_keywords = ["密码错误", "账号或密码不正确"]
        # 检查Toast是否包含任意预期关键词
        assert any(keyword in toast_text for keyword in expected_keywords), \
            f"""
            ❌ 断言失败！
            预期Toast包含：{expected_keywords}
            实际Toast文本：{toast_text}
            """
        # 只有断言成功才会执行这行（显性成功提示）
        print("✅ 断言成功！Toast文本符合预期！")
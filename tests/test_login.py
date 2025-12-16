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

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from pages.login_page import LoginPage
from utils.yaml_utils import YamlUtils

# 加载测试数据
test_data = YamlUtils.load_data("login_data.yaml")


@allure.feature("ShopXO 登录模块")
class TestLogin:

    @allure.story("登录场景覆盖")
    @pytest.mark.parametrize("case_info", test_data)
    def test_login_scenarios(self, page, config, case_info):
        allure.dynamic.title(case_info['case_title'])

        login_page = LoginPage(page)
        login_page.load_locators("login_page.yaml")

        with allure.step(f"访问首页: {config['base_url']}"):
            login_page.goto(config["base_url"])
            login_page.click_login_button()

        with allure.step(f"输入账号: {case_info['username']} / 密码: {case_info['password']}"):
            login_page.input_login_input(case_info['username'])
            login_page.input_password_input(case_info['password'])
            login_page.click_form_login_button()

        # 3. 智能断言逻辑
        if case_info['expect_result'] == 'success':
            with allure.step("验证登录成功"):
                # ✨ 核心修复：不要直接 assert，而是先“等待”关键元素出现
                # 这行代码的意思是：最多等10秒，直到页面上出现包含预期关键词的元素
                try:
                    page.wait_for_selector(f"text={case_info['assert_keyword']}", timeout=10000)
                except Exception:
                    # 如果超时没找到，再截图报错，方便排查
                    allure.attach(page.screenshot(), "失败截图", allure.attachment_type.PNG)
                    raise AssertionError(f"登录超时！页面未找到关键词: {case_info['assert_keyword']}")
        else:
            with allure.step("验证错误提示"):
                # 获取 Toast 本身已经内置了等待，所以这里直接断言即可
                actual_toast = login_page.get_password_error_toast()
                assert case_info['assert_keyword'] in actual_toast, \
                    f"断言失败！预期包含 '{case_info['assert_keyword']}'，实际得到 '{actual_toast}'"
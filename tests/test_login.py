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

# tests/test_login.py
import pytest
import allure
from pages.login_page import LoginPage
from utils.yaml_utils import YamlUtils

# 加载前4条测试数据
login_data = YamlUtils.load_data("login_data.yaml")


@allure.feature("登录/注销模块")
class TestLogin:
    # ================= 登录验证 =================
    @allure.story("登录场景详细测试")
    @pytest.mark.parametrize("case_info", login_data)
    def test_login_scenarios(self, page, config, case_info):
        allure.dynamic.title(case_info['case_title'])

        login_page = LoginPage(page)

        with allure.step("步骤1：打开登录页"):
            login_page.goto(config["base_url"])
            # page.pause()
            login_page.click_login_button()

        with allure.step(f"步骤2：输入账号[{case_info['username']}] 密码[{case_info['password']}]"):
            login_page.input_login_input(case_info['username'])
            login_page.input_password_input(case_info['password'])
            login_page.click_form_login_button()

        # 根据预期结果进行断言
        if case_info['expect_result'] == 'success':
            with allure.step("断言：登录成功"):
                # 等待页面出现“退出”字样，说明登录成功
                page.wait_for_selector(f"text={case_info['assert_keyword']}")
        else:
            with allure.step(f"断言：报错提示包含 [{case_info['assert_keyword']}]"):
                actual_msg = login_page.get_error_message()
                assert case_info['assert_keyword'] in actual_msg

    # ================= 场景 5：退出登录（单独测试） =================
    @allure.story("退出登录测试")
    def test_logout(self, page, config):
        """
        退出登录的测试逻辑：
        1. 先执行登录（必须先登录才能退）
        2. 点击退出
        3. 断言退出成功
        """
        login_page = LoginPage(page)

        # --- 前置：先登录 (这里硬编码一个正确的账号，或者读取配置) ---
        with allure.step("前置：先执行登录"):
            login_page.goto(config["base_url"])
            login_page.click_login_button()
            login_page.input_login_input("qa1234")  # 填入正确账号
            login_page.input_password_input("123456")  # 填入正确密码
            login_page.click_form_login_button()
            # 确保登录成功，看到了“退出”按钮
            page.wait_for_selector("text=退出")

        # --- 核心步骤：点击退出 ---
        with allure.step("步骤：点击退出按钮"):
            login_page.click_logout()

        # --- 断言：验证是否回到未登录状态 ---
        with allure.step("断言：退出成功"):
            # 方式1：验证页面上出现了“登录”按钮
            page.wait_for_selector("text=登录")
            # 方式2：或者验证提示文本（如果有）
            # actual_msg = login_page.get_error_message()
            # assert "退出成功" in actual_msg
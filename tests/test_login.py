#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/10/18 21:25
# @Author  : 地核桃
# @file: test_login.py.py
# @desc:

import pytest
import allure
from pages.login_page import LoginPage
from utils.yaml_utils import YamlUtils

# 去读login_data.yaml
login_data = YamlUtils.load_data("login_data.yaml")


@allure.feature("登录")
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

        # 拿预期结果进行断言
        if case_info['expect_result'] == 'success':
            with allure.step("断言：登录成功"):
                page.wait_for_selector(f"text={case_info['assert_keyword']}")
        else:
            with allure.step(f"断言：报错提示包含 [{case_info['assert_keyword']}]"):
                actual_msg = login_page.get_error_message()
                assert case_info['assert_keyword'] in actual_msg

    # =================退出登录 =================
    @allure.story("退出登录测试")
    def test_logout(self, page, config):
        """
        退出登录的测试逻辑：
        1. 先执行登录（必须先登录才能退）
        2. 点击退出
        3. 断言退出成功
        """
        login_page = LoginPage(page)
        with allure.step("前置：先执行登录"):
            login_page.goto(config["base_url"])
            login_page.click_login_button()
            login_page.input_login_input("qa1234")
            login_page.input_password_input("123456")
            login_page.click_form_login_button()
            page.wait_for_selector("text=退出")
        # --- 点击退出 ---
        with allure.step("步骤：点击退出按钮"):
            login_page.click_logout()

        with allure.step("断言：退出成功"):
            # 方法1：验证页面上出现了“登录”按钮
            page.wait_for_selector("text=登录")
            login_page.log("断言成功：页面已成功跳转回未登录状态，检测到'登录'按钮")
            # 方法2：验证页面上没有出现“退出”按钮，试试不知道能不能拿到
            # actual_msg = login_page.get_error_message()
            # assert "退出成功" in actual_msg
            # login_page.log("断言成功：页面已成功跳转回未登录状态，检测到'登录'按钮")
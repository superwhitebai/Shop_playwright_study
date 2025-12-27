#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/24 19:23
# @Author  : 地核桃
# @file: test_register.py.py
# @desc:
import pytest
import allure
import time
from pages.register_page import RegisterPage
from utils.yaml_utils import YamlUtils

# 加载数据
register_data = YamlUtils.load_data("register_data.yaml")


@allure.feature("注册模块")
class TestRegister:

    @allure.story("新用户注册场景")
    @pytest.mark.parametrize("case_info", register_data)
    def test_register_success(self, page, config, case_info):
        allure.dynamic.title(case_info['case_title'])
        register_page = RegisterPage(page)
        register_page.goto(config['base_url'])
        register_page.click_enter_register()
        unique_username = f"{case_info['username_prefix']}_{int(time.time())}"


        register_page.input_username(unique_username)
        register_page.input_password(case_info['password'])
        register_page.click_register_submit()

        # 6. 断言
        if case_info['expect_result'] == 'success':
            with allure.step("验证注册成功"):
                page.wait_for_selector("text=注册成功")
        else:
            with allure.step("验证注册失败提示"):
                actual_msg = register_page.get_prompt_message()
                assert case_info['assert_keyword'] in actual_msg
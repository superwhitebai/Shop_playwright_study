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

        # 1. 初始化页面
        register_page = RegisterPage(page)

        # 2. 打开首页 (从 config 读取 base_url)
        register_page.goto(config['base_url'])

        # 3. 点击进入注册页
        register_page.click_enter_register()

        # 4. 生成唯一用户名 (Wenl + 时间戳)
        # 这样每次运行都是新账号，不会报“账号已存在”
        unique_username = f"{case_info['username_prefix']}_{int(time.time())}"

        # 5. 执行注册操作
        register_page.input_username(unique_username)
        register_page.input_password(case_info['password'])
        register_page.click_register_submit()

        # 6. 断言
        if case_info['expect_result'] == 'success':
            with allure.step("验证注册成功"):
                # ✨ 成功的时候，去调用新写的 get_success_message
                # 这种文本定位法不需要你去查元素的 class，只要页面上有这几个字就能找到
                # 注意：如果 YAML 里还没配 register_success_toast，直接在这写 locator="text=注册成功" 也可以调试
                page.wait_for_selector("text=注册成功")
        else:
            with allure.step("验证注册失败提示"):
                # 失败的时候，还是找原来的红色框框
                actual_msg = register_page.get_prompt_message()
                assert case_info['assert_keyword'] in actual_msg
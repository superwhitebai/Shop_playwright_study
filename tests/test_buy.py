#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/27 17:05
# @Author  : 地核桃
# @file: test_buy.py.py
# @desc:

import pytest
import allure
from pages.buy_page import HomePage, GoodsDetailPage, OrderConfirmPage
from pages.login_page import LoginPage
from utils.yaml_utils import YamlUtils

buy_data = YamlUtils.load_data("buy_data.yaml")


@allure.feature("购物流程测试")
class TestBuy:

    @allure.story("搜索-加购-下单全流程")
    @pytest.mark.parametrize("case_info", buy_data)
    def test_buy_flow(self, page, config, case_info):
        login_page = LoginPage(page)
        login_page.goto(config['base_url'] + "/index.php?s=/index/user/logininfo.html")
        login_page.input_login_input("qa1234")
        login_page.input_password_input("123456")
        login_page.click_form_login_button()


        home_page = HomePage(page)
        home_page.goto(config['base_url'])
        home_page.search_goods(case_info['search_keyword'])
        home_page.scroll_page_down()
        new_tab = home_page.click_product()

        goods_page = GoodsDetailPage(new_tab)
        goods_page.click_increase_quantity()

        # --- 断言 1: 加入购物车 ---
        goods_page.click_add_to_cart()
        with allure.step("断言: 验证加入购物车提示"):

            toast_text = goods_page.get_add_cart_toast_text()
            assert "加入成功" in toast_text

        goods_page.click_buy_now()
        order_page = OrderConfirmPage(new_tab)
        order_page.click_use_new_address()
        order_page.fill_new_address(
            alias=case_info['addr_alias'],
            name=case_info['addr_name'],
            tel=case_info['addr_tel'],
            province=case_info['addr_province'],
            city=case_info['addr_city'],
            district=case_info['addr_district'],
            detail=case_info['addr_detail']
        )

        with allure.step("断言: 页面包含'快递邮寄'选项"):
            is_exist = order_page.is_express_shipping_visible()
            assert is_exist == True, "未找到'快递邮寄'链接，可能未跳转到确认订单页"

        order_page.select_cod_payment()
        new_tab.wait_for_timeout(500)
        order_page.click_submit_order()
        with allure.step("断言: 订单提交成功提示"):
            # 捕获 "提交成功"
            final_msg = order_page.get_submit_result_text()
            assert "提交成功" in final_msg
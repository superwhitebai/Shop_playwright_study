#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2025/12/27 17:05
# @Author  : 地核桃
# @file: buy_page.py.py
# @desc:
# pages/buy_page.py
import allure
from pages.base_page import BasePage


# === 首页对象 ===
class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.load_locators("buy_page.yaml")
        # 初始化定位符
        self.search_input_loc = self.locators["search_input"]["locator"]
        self.search_button_loc = self.locators["search_button"]["locator"]
        self.target_product_loc = self.locators["target_product"]["locator"]

    @allure.step("搜索商品: {keyword}")
    def search_goods(self, keyword):
        self.input_text(self.search_input_loc, keyword)
        self.click(self.search_button_loc)
        self.page.wait_for_timeout(2000)  # 搜索后强制等待2秒

    @allure.step("页面向下滑动")
    def scroll_page_down(self):
        # ✨ 这里模拟用户滚轮，向下滑动 600 像素
        self.page.evaluate("window.scrollBy(0, 600)")
        self.page.wait_for_timeout(1000)  # 等一等滑动动画结束

    @allure.step("点击商品并切换到新窗口")
    def click_product(self):
        # 1. 预期会发生新页面弹出
        with self.page.context.expect_page() as new_page_info:
            # 点击商品链接
            self.click(self.target_product_loc)

        # 2. 获取新页面对象
        new_page = new_page_info.value
        new_page.wait_for_load_state()  # 等待页面加载完毕
        return new_page


# === 商品详情页对象 ===
class GoodsDetailPage(BasePage):
    def __init__(self, page):
        # 注意：这里接收的 page 是新窗口的 page
        super().__init__(page)
        self.load_locators("buy_page.yaml")
        self.add_btn_loc = self.locators["quantity_increase_button"]["locator"]
        self.cart_btn_loc = self.locators["add_to_cart_button"]["locator"]
        self.buy_btn_loc = self.locators["buy_now_button"]["locator"]
        self.add_cart_toast_loc = self.locators["add_cart_success_toast"]["locator"]
    @allure.step("增加购买数量 (+)")
    def click_increase_quantity(self):
        self.click(self.add_btn_loc)

    @allure.step("点击加入购物车")
    def click_add_to_cart(self):
        self.click(self.cart_btn_loc)

    @allure.step("获取加入购物车结果提示")
    def get_add_cart_toast_text(self):
        # 等待提示出现 (Toast通常消失得快，所以timeout不要太长，也不要太短)
        self.page.wait_for_selector(self.add_cart_toast_loc, state="visible", timeout=5000)
        return self.page.locator(self.add_cart_toast_loc).text_content()

    @allure.step("点击立即购买")
    def click_buy_now(self):
        self.click(self.buy_btn_loc)


# === 确认订单页对象 ===
class OrderConfirmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.load_locators("buy_page.yaml")
        # 主页面元素
        self.new_addr_btn_loc = self.locators["use_new_address_btn"]["locator"]

        # Iframe 及其内部元素
        self.iframe_loc = self.locators["address_iframe"]["locator"]

        # 表单字段
        self.alias_loc = self.locators["address_alias"]["locator"]
        self.name_loc = self.locators["address_name"]["locator"]
        self.tel_loc = self.locators["address_tel"]["locator"]
        self.detail_loc = self.locators["address_detail"]["locator"]
        self.save_btn_loc = self.locators["save_address_btn"]["locator"]

        # 下拉框
        self.prov_trigger = self.locators["province_trigger"]["locator"]
        self.city_trigger = self.locators["city_trigger"]["locator"]
        self.dist_trigger = self.locators["district_trigger"]["locator"]
        self.express_link_loc = self.locators["express_shipping_link"]["locator"]
        self.cod_payment_loc = self.locators["payment_cod_item"]["locator"]
        self.submit_btn_loc = self.locators["submit_order_button"]["locator"]
        self.submit_toast_loc = self.locators["submit_success_toast"]["locator"]

    @allure.step("点击使用新地址")
    def click_use_new_address(self):
        self.click(self.new_addr_btn_loc)

    @allure.step("填写地址表单")
    def fill_new_address(self, alias, name, tel, province, city, district, detail):
        # 1. 获取 Iframe 对象 (关键！)
        # frame_locator 不会立即查找，只有后续操作时才会查找
        frame = self.page.frame_locator(self.iframe_loc)

        # 2. 填写普通文本框 (都在 frame 里操作)
        frame.locator(self.alias_loc).fill(alias)
        frame.locator(self.name_loc).fill(name)
        frame.locator(self.tel_loc).fill(tel)

        # 3. 处理级联下拉框 (难点)
        # 逻辑：点击触发器 -> 等待列表出现 -> 点击对应的文字

        # --- 选择省份 ---
        frame.locator(self.prov_trigger).click()  # 点开下拉框
        # 在 frame 里找文本为“安徽省”的元素点击
        # 注意：ShopXO 的下拉选项通常是 li 或 a 标签
        frame.locator(f"li:has-text('{province}')").click()

        # --- 选择城市 (等省份选完，城市列表会自动加载) ---
        self.page.wait_for_timeout(500)  # 稍等联动
        frame.locator(self.city_trigger).click()
        frame.locator(f"li:has-text('{city}')").click()

        # --- 选择区县 ---
        self.page.wait_for_timeout(500)
        frame.locator(self.dist_trigger).click()
        frame.locator(f"li:has-text('{district}')").click()

        # 4. 填写详细地址并保存
        frame.locator(self.detail_loc).fill(detail)
        frame.locator(self.save_btn_loc).click()

    @allure.step("检查'快递邮寄'元素是否存在")
    def is_express_shipping_visible(self):
        # expect_element_visible 是 BasePage 里可能有的，如果没有，用下面的原生写法
        try:
            self.page.locator(self.express_link_loc).wait_for(state="visible", timeout=5000)
            return True
        except:
            return False

    @allure.step("选择货到付款")
    def select_cod_payment(self):
        # 有时候支付方式需要先点一下父级容器，这里直接点 'li' 即可
        self.click(self.cod_payment_loc)

    @allure.step("点击提交订单")
    def click_submit_order(self):
        self.click(self.submit_btn_loc)

    @allure.step("获取提交成功提示")
    def get_submit_result_text(self):
        self.page.wait_for_selector(self.submit_toast_loc, state="visible", timeout=10000)
        return self.page.locator(self.submit_toast_loc).text_content()
# 注册登录测试
from time import sleep

from api.api_register_login import ApiRegisterLogin
import pytest
from tools import clear_data, read_json, common_assert
import requests

class TestRegisterLogin:
    # 登录前先删除数据库中的用户数据
    def setup_class(self):
        clear_data()

    # 初始化（每个测试方法前执行）
    def setup_method(self):
        self.session=requests.session()
        self.api=ApiRegisterLogin(self.session)
    
    # 结束
    def teardown_method(self):
        self.session.close()
    
    # 图片验证码
    @pytest.mark.parametrize("row",read_json("register_login.json","img_code"))
    def test_img_code(self,row):
        resp=self.api.api_img_code(row["random"])
        try:
           common_assert(response=resp,status_code=200)
        except Exception as e:
            raise e
    
    @pytest.mark.parametrize("row",read_json("register_login.json","phone_code"))
    def test_phone_code(self,row):
        # 前置条件，先获取图片验证码，再调用获取短信验证码接口
        self.api.api_img_code(12345)
        resp=self.api.api_phone_code(row["phone"],row["imgVerifyCode"])
        try:
           common_assert(response=resp,expect_json=row["expect_json"])
        except Exception as e:
            raise e
    
    # 注册
    @pytest.mark.parametrize("row",read_json("register_login.json","register"))
    def test03_register(self,row):
        self.api.api_img_code(12345)
        self.api.api_phone_code(phone=row["phone"],imgVerifyCode=row["verifycode"])
        resp=self.api.api_register(phone=row["phone"],password=row["password"],verifycode=row["verifycode"],phone_code=row["phone_code"])
        try:
           common_assert(response=resp,expect_json=row["expect_json"])
        except Exception as e:
            raise e
    
    # 登录
    @pytest.mark.parametrize("row",read_json("register_login.json","login"))
    def test04_login(self,row):
        if row["password"]=="error123":
            i=1
            current_row=row
            while i<=3:
                resp=self.api.api_login(keywords=current_row["keywords"],password=current_row["password"])
                i+=1
            if "锁定" in resp.text:
                sleep(60)
                resp=self.api.api_login(keywords="13600001111",password="test123")
                try:
                   common_assert(response=resp,expect_json="成功")
                except Exception as e:
                    raise e
        else:
            resp=self.api.api_login(keywords=row["keywords"],password=row["password"])
            try:
               common_assert(response=resp,expect_json=row["expect_json"])
            except Exception as e:
                raise e
    
    # 查询是否登录
    @pytest.mark.parametrize("row",read_json("register_login.json","login_status"))
    def test05_login_status(self,row):
        self.api.api_login(keywords="13600001111",password="test123")
        resp=self.api.api_login_status()
        try:
           common_assert(response=resp,expect_json=row["expect_json"])
        except Exception as e:
            raise e
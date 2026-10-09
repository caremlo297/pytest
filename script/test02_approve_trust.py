import pytest
import requests
from api.api_approve_trust import ApiApproveTrust
from api.api_register_login import ApiRegisterLogin
from tools import common_assert, parse_html, read_json

class TestApproveTrust:
    def setup_method(self):
        self.session=requests.session()
        self.api=ApiApproveTrust(self.session)
        ApiRegisterLogin(self.session).api_login()
    
    def teardown_method(self):
        self.session.close()

    @pytest.mark.parametrize("row",read_json("approve_trust.json","approve"))
    def test01_approve(self,row):
        resp=self.api.api_approve(row["realname"],row["card_id"])
        common_assert(response=resp,expect_json=row["expect_json"])
    
    def test02_approve_status(self):
        self.api.api_approve()
        resp=self.api.api_approve_status()
        common_assert(response=resp,status_code=200)

    def test03_api_trust(self):
        resp=self.api.api_trust()
        common_assert(response=resp,status_code=200)
        action_url,form_params=parse_html(resp)
        response=requests.post(action_url,data=form_params)
        common_assert(response=response,status_code=200)

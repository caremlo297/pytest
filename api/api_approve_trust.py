import base64
import base64
from config import HOST
class ApiApproveTrust:
    def __init__(self,session):
        self.session=session
        # 实名认证
        self.__url__approve=HOST+"/member/realname/approverealname"
        # 获取认证信息
        self.__url__approve_status=HOST+"/member/member/getapprove"
        # 开户url
        self.__url_trust=HOST+"/trust/trust/register"

    def api_approve(self,realname="张三",card_id="110101201703072050"):
        data={
            "realname":realname,
            "card_id":card_id
        }
        return self.session.post(url=self.__url__approve,data=data,files={"x": "y"})
    
    def api_approve_status(self):
        return self.session.post(url=self.__url__approve_status)

    def api_trust(self):
        return self.session.post(url=self.__url_trust)
from config import HOST


class ApiRegisterLogin:
    def __init__(self,session):
        self.session=session
        # 获取图片验证码
        self.__url_img_code=HOST+"/common/public/verifycode1/{r}"
        # 获取短信验证码
        self.__url_phone_code=HOST+"/member/public/sendSms"
        # 注册
        self.__url_register=HOST+"/member/public/reg"
        # 登录
        self.__url_login=HOST+"/member/public/login"
        # 查询是否登录
        self.__url_login_status=HOST+"/member/public/islogin"

    # 调用获取图片验证码接口
    def api_img_code(self,random):
        return self.session.get(self.__url_img_code.format(r=random))

    # 获取短信验证码
    def api_phone_code(self,phone,imgVerifyCode):
        data={
            "phone":phone,
            "imgVerifyCode":imgVerifyCode,
            "type":"reg"
        }
        # data默认请求头的content_type为application/x-www-form-urlencoded
        return self.session.post(self.__url_phone_code,data=data)
    
    # 注册
    def api_register(self,phone,password,verifycode,phone_code):
        data={
            "phone":phone,
            "password":password,
            "verifycode":verifycode,
            "phone_code":phone_code,
            "dy_server":"on",
            "invite_phone":""
        }
        return self.session.post(self.__url_register,data=data)
    
    # 登录
    def api_login(self,keywords="13600001111",password="test123"):
        data={
            "keywords":keywords,
            "password":password
        }
        return self.session.post(self.__url_login,data=data)
    
    def api_login_status(self):
        return self.session.post(self.__url_login_status)
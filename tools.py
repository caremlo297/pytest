import os
import json
from bs4 import BeautifulSoup

from config import DIR_PATH

# 读取json数据中的数据供pytest用[{},{}]
def read_json(file_name,key):
   file_path=DIR_PATH+os.sep+"data"+os.sep+file_name
   with open(file_path,"r",encoding="utf-8") as f:
       data=json.load(f)
       return data[key]

# 断言
def common_assert(response,status_code=None,expect_json=None,expect_text=None):
    if status_code:
        assert response.status_code == status_code,"预期状态码：{}!=实际状态码：{}".format(status_code,response.status_code)
    if expect_json:
        assert expect_json in response.json().get("description"),"实际结果：{}不包含预期结果：{}".format(response.json().get("description"),expect_json)
    if expect_text:
        assert expect_text in response.text,"实际结果：{}不包含预期结果：{}".format(response.text,expect_text)

# 解析html响应体，测试第三方
def parse_html(response):
    print(response.json())
    soup=BeautifulSoup(response.json().get("description").get("form"),"html.parser")
    form_tag = soup.find("form")

    # 提取form action
    action_url = form_tag["action"]

    # 提取所有input标签，组装name:value字典
    form_params = {}
    input_list = form_tag.find_all("input")
    for input_tag in input_list:
        name = input_tag.get("name")
        value = input_tag.get("value", "")
        form_params[name] = value
    return action_url,form_params

# 连接数据库工具
def connect_mysql(sql):
    conn = None
    cursor = None
    try:
        # 获取连接对象
        conn = pymysql.connect(host="121.43.169.97",
                               user="student",
                               password="P2P_student_2023",
                               database="czbk_member",
                               port=3306,
                               charset="utf8",
                               autocommit=True)
        # 获取游标对象
        cursor = conn.cursor()
        # 执行sql语句
        cursor.execute(sql)
        # 返回什么结果
        if sql.lower().split()[0] == "select":
            # 查询返回所有数据
            return cursor.fetchall()
        else:
            # 非查询返回受影响的行数
            return cursor.rowcount
    except Exception as e:
        print("出错了：",e)
        # 回滚
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 清楚数据
def clear_data():
    sql_1 = """
        delete info.* from mb_member as mb inner join mb_member_info  as info on info.member_id = mb.id where mb.phone in ("13600001111","13600001112","13600001113","13600001114");
    """
    connect_mysql(sql_1)
    sql_2 = """
        delete login.* from mb_member as mb inner join mb_member_login_log  as login on login.member_id = mb.id where mb.phone in ("13600001111","13600001112","13600001113","13600001114");
        """
    connect_mysql(sql_2)
    sql_3 = """
        delete from mb_member where phone in ("13600001111","13600001112","13600001113","13600001114");
        """
    connect_mysql(sql_3)
    sql_4 = """
        delete from mb_member_register_log where phone in ("13600001111","13600001112","13600001113","13600001114");
        """
    connect_mysql(sql_4)
import os
HOST="http://121.43.169.97:8081"
# 获取该文件所在目录的父级路径
DIR_PATH=os.path.dirname(__file__)

# 第三方开户接口地址（汇付天下测试环境）
THIRD_PARTY_URL="http://mertest.chinapnr.com/muser/publicRequests"
# 商户私钥文件路径（PKCS#8 PEM 格式，需自行放入 keys 目录）
PRIVATE_KEY_PATH=DIR_PATH+os.sep+"keys"+os.sep+"mer_private_key.pem"

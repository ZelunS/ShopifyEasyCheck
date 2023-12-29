import requests
import time
import hashlib
import base64
import hmac
from datetime import datetime

def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

def time10():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    ts10 = str(timestamp).split('.')[0]
    return ts10

# def sendMsg():
#     url = "https://open.feishu.cn/open-apis/bot/v2/hook/d8a6f124-7be7-48fe-b24c-d1eb08242833"
#     data = {
#         "timestamp":str(time10()),
#         # "sign":"4DtxiISKlOH1c5LSMBMXrb",
#         "sign": gen_sign(time10(),"4DtxiISKlOH1c5LSMBMXrb"),
#         "msg_type": "text",
#         "content": {"text": "request example"}
#     }
#     headers = {"Content-Type":"application/json"}
#     rep = requests.post(url, json=data,headers=headers)
#     print(rep.json())
#     print(data)

def sendMsg():
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/d8a6f124-7be7-48fe-b24c-d1eb08242833"
    data = {
        "timestamp":str(time10()),
        # "sign":"4DtxiISKlOH1c5LSMBMXrb",
        "sign": gen_sign(time10(),"4DtxiISKlOH1c5LSMBMXrb"),
        "msg_type": "post",
        "content": {
		    "post": {
			    "zh_cn": {
				    "title": "折扣码异常",
				    "content": [
					    [{
							        "tag": "text",
							        "text": "幸运转盘有折扣码异常: "
						    },
						    {
							        "tag": "a",
							        "text": "请查看",
							        "href": "https://admin.shopify.com/login"
						    },
					    ]
				    ]
			    }
		    }
	    }
    }
    headers = {"Content-Type":"application/json"}
    rep = requests.post(url, json=data,headers=headers)
    print(rep.json())
    print(data)

if __name__ == '__main__':
    sendMsg()






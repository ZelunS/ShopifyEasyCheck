import base64
import datetime
import hashlib
import hmac
import time
import aiohttp
import asyncio


def gen_sign(timestamp, secret):
    """
    获取飞书签名
    """
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign


async def get_feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    json_data = {
        "app_id": "cli_a36a68804f7b500e",
        "app_secret": "6r0t2OR8orvYB8ERfXpmMclE5eYqy8Qp"
    }
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data, headers=headers) as res:
            # 检查响应状态码
            if res.status != 200:
                # 请求失败，打印错误信息
                print("Request failed with status code:", res.status)
                text = await res.text()
                print("Error message:", text)

            return await res.json()


async def get_feishu_user_id(token: str, email: list):
    url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
    json_data = {
        "emails": email,
        "include_resigned": True
    }
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data, headers=headers) as res:
            # 检查响应状态码
            if res.status != 200:
                # 请求失败，打印错误信息
                print("Request failed with status code:", res.status)
                text = await res.text()
                print("Error message:", text)

            json_res = await res.json()
            users = json_res.get('data').get('user_list')
            return {user.get('email'): user.get('user_id') for user in users}


async def send_notify(todo_user, todo_user_email, content, feishu_notify_url, feishu_notify_sign):
    """发送飞书通知"""
    try:
        feishu_token = await get_feishu_token()
        feishu_users = await get_feishu_user_id(feishu_token.get('app_access_token'), [todo_user_email])
        feishu_user_id = feishu_users.get(todo_user_email)
        print(feishu_user_id)

        timestamp = int(time.time())
        sign = gen_sign(timestamp, feishu_notify_sign)

        headers = {"Content-Type": "application/json"}
        json_data = {
            "timestamp": f"{timestamp}",
            "sign": f"{sign}",
            "msg_type": "interactive",
            "card": {
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": f"- 待办人：{todo_user}",
                            "tag": "plain_text"
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "content": f"- 内容：{content}",
                            "tag": "plain_text"
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "content": f"- 时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            "tag": "plain_text"
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "content": f'<at id="{feishu_user_id}">at{todo_user}</at>',
                            "tag": "lark_md"
                        }
                    }
                ],
                "header": {
                    "template": "blue",
                    "title": {
                        "content": "DataX通知",
                        "tag": "plain_text"
                    }
                }
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(feishu_notify_url, json=json_data, headers=headers) as res:
                # 检查响应状态码
                if res.status != 200:
                    # 请求失败，打印错误信息
                    print("Request failed with status code:", res.status)
                    text = await res.text()
                    print("Error message:", text)
                print("将feedback info 推送到飞书")
    except Exception as e:
        pass


if __name__ == '__main__':
    feishu_notify_url = "https://open.feishu.cn/open-apis/bot/v2/hook/e7880e1a-2e1a-44a2-8254-6a9089bee760"
    feishu_notify_sign = "mVSTRaZsixBPpCb5lI9efb"
    asyncio.run(send_notify("Sun Kang", "kang.sun@amperetime.com", "content", feishu_notify_url, feishu_notify_sign))

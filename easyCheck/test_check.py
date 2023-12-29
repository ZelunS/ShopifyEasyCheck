import pytest
import requests
import jsonpath
from sendMsg import sendMsg

class TestCheck:

    token = ""
    id = ""

    def test_token(self):
        url = "https://api.askstarry.com/shopify/app/auth"
        data = {
            "secret":"562bb14b557f803d35f0302c5907cba7",
            "shop":"litime-us.myshopify.com"
        }
        rep = requests.post(url,json=data)
        print(rep.json())
        TestCheck.token = rep.json()['data']['token']


    def test_getCampaign(self):
        url = "https://api.askstarry.com/shopify/app/campaign"
        params = {
            "page":1,
            "per_page":10
        }
        headers = {"Authorization":"Bearer "+TestCheck.token}
        rep = requests.get(url=url,params=params,headers=headers)
        print(rep.json())
        assert rep.json()['message'] == "成功"
        if rep.json()['data']['records'][0]['status'] == 1:
            TestCheck.id = rep.json()['data']['records'][0]['id']
        else:
            print("没有活动开启")

    def test_getDetail(self):
        url = "https://api.askstarry.com/shopify/app/campaign/"+str(TestCheck.id)+"/lottery_detail"
        params = {
            "page":1,
            "per_page":10
        }
        headers = {"Authorization":"Bearer "+TestCheck.token}
        rep = requests.get(url=url,params=params,headers=headers)
        print(rep.json())
        status = jsonpath.jsonpath(rep.json(),'$.data.records[*].status')
        # print(status)
        for i in status:
            if i == 2:
                sendMsg()
                print("有折扣码异常")
            else:
                break


if __name__ == '__main__':
    pytest.main(['-vs'])

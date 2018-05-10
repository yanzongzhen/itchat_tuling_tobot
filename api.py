import requests
import json
import time
import hashlib

class TulingConf:
    def __init__(self,appKey,appSecret):
        self.api_host = 'http://openapi.tuling123.com/openapi/api/v2'
        self.appSecret = appSecret
        self.appKey = appKey


class TulingBase:
    def __init__(self, conf: TulingConf):
        self.appSecret = conf.appSecret
        self.appKey = conf.appKey
        self.api_host = conf.api_host

    def sign(self, params):
        timestamp = int(time.time())
        params["timestamp"] = timestamp
        params['token'] = hashlib.md5(self.appSecret.encode('utf-8')+str(timestamp).encode('utf-8')).hexdigest()
        return params


class TulingService(TulingBase):    
    def __init__(self, conf: TulingConf):
        super().__init__(conf)

    def get_data(self,text):
        userId = '123456'
        inputText = {'text': text}
        key = self.appKey
        userInfo = {'apiKey': key, 'userId': userId}
        perception = {'inputText': inputText}
        data = {'perception': perception, 'userInfo': userInfo,'reqType':0}
        return data

    def get_pic_data(self,pic_url):
        userId = '123456'
        key = self.appKey
        userInfo = {'apiKey': key, 'userId': userId}
        perception = {'inputImage': {"url": pic_url}}
        data = {'perception': perception, 'userInfo': userInfo,'reqType':1}
        return data

    def get_answer(self,text):
        data = self.get_data(text)
        res = requests.post(url=self.api_host,data=json.dumps(data),headers={'Content-Type':'application/json'})
        res_dict = json.loads(res.text)
        if res.status_code == 200:
            if len(res_dict.get('results')) >= 1:
                for i in range(len(res_dict.get('results'))):
                    answer = res_dict.get('results')[i].get('values').get('text')
                    return answer
        else:
            return 'erorr'

    def get_answer_pic(self, pic_url):
        data = self.get_pic_data(pic_url)
        res = requests.post(url=self.api_host,data=json.dumps(data),headers={'Content-Type':'application/json'})
        res_dict = json.loads(res.text)
        if res.status_code == 200:
            if len(res_dict.get('results')) >= 1:
                for i in range(len(res_dict.get('results'))):
                    answer = res_dict.get('results')[i].get('values').get('image')
                    return answer
        else:
            return 'erorr'


if __name__ == "__main__":
    conf = TulingConf('2b902a5a9cb741abafd33928bfc0c536','3a20af4af4318431')
    TBS = TulingService(conf)
    
    urls = 'http://file.tuling123.com/upload/image/201805/60ba2833-d119-4fe4-8881-180e9f78808f.jpg'
    print(TBS.get_answer_pic(urls))
    print(TBS.get_answer('滕州的天气'))
        
            
    
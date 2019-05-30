# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-05-14 17:40
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-14 17:40'

import execjs
import requests
import re
from SuTranslate.UserAgentInfos import UserAgentInfos

JS_CODE = """
function a(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var a = o.charAt(t + 2);
        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
        a = "+" === o.charAt(t + 1) ? r >>> a: r << a,
        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
    }
    return r
}
var C = null;
var token = function(r, _gtk) {
    var o = r.length;
    o > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substring(r.length, r.length - 10));
    var t = void 0,
    t = null !== C ? C: (C = _gtk || "") || "";
    for (var e = t.split("."), h = Number(e[0]) || 0, i = Number(e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) {
        var m = r.charCodeAt(g);
        128 > m ? d[f++] = m: (2048 > m ? d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128)
    }
    for (var S = h,
    u = "+-a^+6",
    l = "+-3^+b+-f",
    s = 0; s < d.length; s++) S += d[s],
    S = a(S, u);
    return S = a(S, l),
    S ^= i,
    0 > S && (S = (2147483647 & S) + 2147483648),
    S %= 1e6,
    S.toString() + "." + (S ^ h)
}
"""


class BaiDuTranslator:
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {'User-Agent': UserAgentInfos.GetUserAgent()}
        self.token = None
        self.gtk = None
        self.TryNum = 0
        # 获得token和gtk
        # 必须要加载两次保证token是最新的，否则会出现998的错误
        self.loadMainPage()
        self.loadMainPage()

    def loadMainPage(self):
        """
            load main page : https://fanyi.baidu.com/
            and get token, gtk
        """
        url = 'https://fanyi.baidu.com'

        try:
            r = self.sess.get(url, headers=self.headers)
            # print(r.request.headers)
            self.token = re.findall(r"token: '(.*?)',", r.text)[0]  # if re.findall(r"token: '(.*?)',", r.text) else ""
            self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[
                0]  # if re.findall(r"window.gtk = '(.*?)';", r.text) else ""
        except IndexError:
            import time
            self.TryNum += 1
            if self.TryNum > 2:
                return "尝试超过2次"
            self.loadMainPage()
        except Exception as e:
            raise e
            # print(e)

    def langdetect(self, query):
        """
            post query to https://fanyi.baidu.com/langdetect
            return json
            {"error":0,"msg":"success","lan":"en"}
        """
        url = 'https://fanyi.baidu.com/langdetect'
        data = {'query': query}
        try:
            r = self.sess.post(url=url, data=data)
        except Exception as e:
            raise e
            # print(e)

        json = r.json()
        if 'msg' in json and json['msg'] == 'success':
            return json['lan']
        return None

    def dictionary(self, query):
        """
            max query count = 2
            get translate result from https://fanyi.baidu.com/v2transapi
        """
        url = 'https://fanyi.baidu.com/v2transapi'

        sign = execjs.compile(JS_CODE).call('token', query, self.gtk)

        lang = self.langdetect(query)
        data = {
            'from': 'en' if lang == 'en' else 'zh',
            'to': 'zh' if lang == 'en' else 'en',
            'query': query,
            'simple_means_flag': 3,
            'sign': sign,
            'token': self.token,
        }
        try:
            r = self.sess.post(url=url, data=data)
            # print(r.request.headers)
        except Exception as e:
            raise e

        if r.status_code == 200:
            json = r.json()
            if 'error' in json:
                raise Exception('baidu sdk error: {}'.format(json['error']))
                # 998错误则意味需要重新加载主页获取新的token
            return json
        return None

    def dictionary_by_lang(self, query, fromlang="en", tolang="zh"):
        """
            max query count = 2
            get translate result from https://fanyi.baidu.com/v2transapi
        """
        url = 'https://fanyi.baidu.com/v2transapi'

        sign = execjs.compile(JS_CODE).call('token', query, self.gtk)
        # print(sign)
        # lang = self.langdetect(query)
        data = {
            'from': fromlang,
            'to': tolang,
            'query': query,
            'simple_means_flag': 3,
            'sign': sign,
            'token': self.token
        }

        try:
            r = self.sess.post(url=url, data=data)
            # print(r.request.headers)
        except Exception as e:
            raise e
        if r.status_code == 200:
            json = r.json()
            if 'error' in json:
                return {'error': 2, 'msg': '百度接口出现998,翻译被封,稍后尝试!'}
                # raise Exception('baidu sdk error: {}'.format(json['error']))
                # 998错误则意味需要重新加载主页获取新的token
            else:
                return {'error': 0, 'msg': '百度接返回成功', 'result': json["trans_result"]["data"][0]['dst']}

    def translate(self, text):
        result = self.dictionary_by_lang(text)
        if int(result['error']) > 0:
            return {"error": 1, "msg": "百度翻译失败"}
        return {"error": 0, "msg": "百度翻译成功", "result": result['result']}


if __name__ == '__main__':
    from SuTranslate.Logger import Logger

    try:
        r = BaiDuTranslator().translate("test")
    except Exception as e:
        Logger().exception(e)
        exit(1)
    else:
        Logger().info(r)

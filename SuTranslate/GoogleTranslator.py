# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 广医五院  志明  2019-05-17 10:28
# 当前计算机登录名称 :andy
# 项目名称  :andy
# 编译器   :PyCharm
__author____ = '志明'
__time__ = '2019-05-17 10:28'

import logging
import execjs
import requests


class GoogleTranslator(object):
    GoogleJSCode = """
    function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 

        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 

        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 

    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """

    def __init__(self) -> None:
        super().__init__()
        self.__ctx = execjs.compile(GoogleTranslator.GoogleJSCode)

    def translate(self, text):
        tk = self.__ctx.call("TL", text)
        param = {'tk': tk, 'q': text}
        try:
            result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en 
                &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
                &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)
        # 返回的结果为Json，解析为一个嵌套列表
        except Exception as e:
            print(e)
            return {"Status": 2, "Desc": "谷歌翻译过程中出现异常!", "Result": None}
        except KeyboardInterrupt as e:
            print("用户中断")
        except SystemExit:
            print("系统退出!")
        else:
            trans = result.json()[0]
            ret = ''
            for i in range(len(trans)):
                line = trans[i][0]
                if line != None:
                    ret += trans[i][0]

            if ret:
                return {"error": 0, "msg": "谷歌翻译成功", "result": ret}
            return {"error": 1, "msg": "谷歌翻译失败"}


if __name__ == '__main__':
    print(GoogleTranslator().translate("Secure Sockets Layer (SSL)"))

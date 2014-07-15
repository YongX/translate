# -*- coding: utf-8 -*-

__author__ = 'Terrible Ghost'

import urllib.request
import urllib.parse
import http.client
import re
import time


class Translation:
    """调用google翻译的一个小工具，为访问不到google页面的人士准备
    _target_lang: 需要翻译成的语言
    _source_lang: 需要被翻译的语言
    _text: 需要翻译的文本内容
    _file: 需要保存的文件名
    """

    def __init__(self, target_language="zh-CN", source_language="en", text="Hello World!", file=""):
        self._host = "translate.google.cn"
        self._method = "GET"
        self._request_url = "/translate_a/t"
        self._target_lang = target_language
        self._source_lang = source_language
        self._text = text
        self._param = urllib.parse.urlencode({
            "client": "t",
            "sl": self._source_lang,
            "tl": self._target_lang,
            "hl": "zh-CN",
            "sc": "2",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "oc": "1",
            "otf": "2",
            "ssel": "0",
            "tsel": "0",
            "prev": "btn",
            "q": self._text
        })
        self._file = file
        # 测试连接性
        self.test_conn()

    def get_target_lang(self):
        return self._target_lang

    def get_source_lang(self):
        return self._source_lang

    def get_test(self):
        return self._text

    def set_target_lang(self, tl="en"):
        self._target_lang = tl
        self.update_param()
        return self

    def set_source_lang(self, sl="zh-CN"):
        self._source_lang = sl
        self.update_param()
        return self

    def set_text(self, text):
        self._text = text
        self.update_param()
        return self

    def update_param(self):
        self._param = urllib.parse.urlencode({
            "client": "t",
            "sl": self.get_source_lang(),
            "tl": self.get_target_lang(),
            "hl": "zh-CN",
            "sc": "2",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "oc": "1",
            "otf": "2",
            "ssel": "0",
            "tsel": "0",
            "prev": "btn",
            "q": self.get_test()
        })
        return True

    def test_conn(self):
        stime = time.time()
        conn = http.client.HTTPConnection(self._host)
        conn.request(self._method, self._request_url + "?" + self._param)
        data = conn.getresponse()
        etime = time.time()
        if data.status == 200:
            print("连接成功，延迟约为：" + str(round(((etime - stime) * 1000), 0)) + "ms")
        else:
            print("连接失败，无法进行翻译")

    def start(self):
        if len(self._target_lang) > 1:
            param_queue = []
            for tl in self._target_lang:
                param = urllib.parse.urlencode({
                    "client": "t",
                    "sl": self.get_source_lang(),
                    "tl": tl,
                    "hl": "zh-CN",
                    "sc": "2",
                    "ie": "UTF-8",
                    "oe": "UTF-8",
                    "oc": "1",
                    "otf": "2",
                    "ssel": "0",
                    "tsel": "0",
                    "prev": "btn",
                    "q": self.get_test()
                })
                param_queue.append(param)

    def trans(self):
        conn = http.client.HTTPConnection(self._host)
        conn.request(self._method, self._request_url + "?" + self._param)
        response = conn.getresponse().read().decode("utf-8")
        result = re.findall(r'"(.*?)"', response)
        if self._file:
            with open(self._file, "a+", encoding="utf-8") as f:
                print(self._text, file=f)
                print(result[0], file=f)
            print("处理完成")
        else:
            print(self._text)
            print(result[0])
        conn.close()
        return self


if __name__ == "__main__":
    """google翻译v0.1版本
    usage: trans = Translation([target_language][, source_language][, text][, file])

    target_language 默认为en（英语）
    source_language 默认为zh-CN（中文）
    text            默认为”hello world“
    file            设置其值的话，内容将会保存到file文件中（需自己指定后缀名）。模式为a+

    sample:
    translate = Translation("en", "zh-CN", "Hello World")
    >>> 连接成功，延迟为：xxxms
    >>> 你好世界

    目标语言对照表(部分):
    targetLanguage = {
        'bg': '保加利亚语',
        'zh-CN': '中文简体',
        'de': '德语',
        'nl': '荷兰语',
        'et': '爱沙尼亚语',
        'en': '英语',
        'es': '西班牙语',
        'fr': '法语',
        'it': '意大利语',
        'ja': '日语',
        'ko': '韩语',
        'pt': '葡萄牙语',
        'pt': '葡萄_巴西语',
        'zh-TW': '繁体中文'
    }
    """
    translate = Translation()
    translate.set_source_lang("en").set_target_lang("zh-CN").set_text("hello")
    translate.trans()
    translate.set_text("Who are you").trans().set_target_lang("zh-TW").trans().set_target_lang("pt").trans()

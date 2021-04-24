# encoding=utf-8

from google_trans_new import google_translator
from sim_cilin import *
from sim_hownet import *
from sim_simhash import *
from sim_tokenvector import *
from sim_vsm import *
import http.client
import hashlib
from urllib import parse
import random
import json
import numpy as np
import baiduapi

cilin = SimCilin()
hownet = SimHownet()
simhash = SimHaming()
simtoken = SimTokenVec()
simvsm = SimVsm()




def baidu_translate_text(q, fromLang = 'en', toLang = 'zh'):

    httpClient = None
    myurl = '/api/trans/vip/translate'
    appid = baiduapi.appid
    secretKey = baiduapi.secretKey

    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        html = response.read().decode('utf-8')
        # print (html)
        html = json.loads(html)
        # print (html)
        dst = html["trans_result"][0]["dst"]
        # print (dst)
    except Exception as e:
        print(e)
        dst = ''
    finally:
        if httpClient:
            httpClient.close()
        return dst


def google_translate_text(text):
    translator = google_translator(timeout=10)
    result = []

    #中-英-中
    en = translator.translate(text, 'en')
    ch_en_ch =translator.translate(en, 'zh-cn')
    ch_en_ch_Baidu = baidu_translate_text(en, fromLang='auto', toLang='zh')
    result.append(ch_en_ch_Baidu)
    result.append(ch_en_ch)


    #中-法-中
    # translator = Translator()
    fr = translator.translate(text, 'fr')
    ch_fr_ch =translator.translate(fr, 'zh-cn')
    ch_fr_ch_Baidu = baidu_translate_text(fr, fromLang='auto', toLang='zh')
    result.append(ch_fr_ch_Baidu)
    result.append(ch_fr_ch)


    #中-德-中
    # translator = Translator()
    de = translator.translate(text, 'de')
    ch_de_ch =translator.translate(de, 'zh-cn')
    ch_de_ch_Baidu = baidu_translate_text(de, fromLang='auto', toLang='zh')
    result.append(ch_de_ch_Baidu)
    result.append(ch_de_ch)


    #中-韩-中
    # translator = Translator()
    ko = translator.translate(text, 'ko')
    ch_ko_ch =translator.translate(ko, 'zh-cn')
    ch_ko_ch_Baidu = baidu_translate_text(ko, fromLang='auto', toLang='zh')
    result.append(ch_ko_ch_Baidu)
    result.append(ch_ko_ch)


    #中-俄-中
    # translator = Translator()
    ru = translator.translate(text, 'ru')
    ch_ru_ch =translator.translate(ru, 'zh-cn')
    ch_ru_ch_Baidu = baidu_translate_text(ru, fromLang='auto', toLang='zh')
    result.append(ch_ru_ch_Baidu)
    result.append(ch_ru_ch)


    #中-西班牙-中
    # translator = Translator()
    es = translator.translate(text, 'es')
    ch_es_ch =translator.translate(es, 'zh-cn')
    ch_es_ch_Baidu = baidu_translate_text(es, fromLang='auto', toLang='zh')
    result.append(ch_es_ch_Baidu)
    result.append(ch_es_ch)


    #中-阿拉伯语-中
    # translator = Translator()
    ar = translator.translate(text, 'ru')
    ch_ar_ch =translator.translate(ar, 'zh-cn')
    ch_ar_ch_Baidu = baidu_translate_text(ar, fromLang='auto', toLang='zh')
    result.append(ch_ar_ch_Baidu)
    result.append(ch_ar_ch)


    #中-日-中
    # translator = Translator()
    ja = translator.translate(text, 'ja')
    ch_ja_ch =translator.translate(ja, 'zh-cn')
    ch_ja_ch_Baidu = baidu_translate_text(ja, fromLang='auto', toLang='zh')
    result.append(ch_ja_ch_Baidu)
    result.append(ch_ja_ch)

    return result


def sim_test(text1, text2):

    sim_result = cilin.distance(text1, text2)

    # sim1 = cilin.distance(text1, text2)
    # sim2 = hownet.distance(text1, text2)
    # sim3 = simhash.distance(text1, text2)
    # sim4 = simtoken.distance(text1, text2)
    # sim5 = simvsm.distance(text1, text2)

    # sim_result = (sim1 + sim2 + sim3 + sim4 + sim5) / 5

    return sim_result


if __name__ == "__main__":
    text = "无所畏惧"
    sim_text = []
    sim_text.append("无所畏惧")



    result = {}
    for x in google_translate_text(text):
        sim_result = []
        if(x):
            for y in sim_text:
                if(y):
                    sim_result.append((sim_test(x, y) * 100))
            mean = int(np.mean(sim_result))
            print(mean, end="  ")
            print(x)








#!/usr/bin/python
# _*_coding:utf-8 _*_

import urllib, urllib2
import json
import sys
import simplejson
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')


def gettoken(corpid, corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    print
    gettoken_url
    try:
        token_file = urllib2.urlopen(gettoken_url)
    except urllib2.HTTPError as e:
        print
        e.code
        print
        e.read().decode("utf8")
        sys.exit()
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token


def senddata(access_token, user, content):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser": user,  # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
        "toparty": "5",  # 企业号中的部门id。
        "msgtype": "text",  # 消息类型。
        "agentid": "1",  # 企业号中的应用id。
        "text": {
            "content": content
        },
        "safe": "0"
    }
    #    send_data = json.dumps(send_values, ensure_ascii=False)
    send_data = simplejson.dumps(send_values, ensure_ascii=False).encode('utf-8')
    send_request = urllib2.Request(send_url, send_data)
    response = json.loads(urllib2.urlopen(send_request).read())
    print(str(response))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--user', type=str, default=None)
    parser.add_argument('--message', type=str, default=None)
    args = parser.parse_args()
    corpid = 'wx9c595e2ff0429f13'  # CorpID是企业号的标识
    corpsecret = 'Ois1toLLjFaJnIN6RppvSafxjSvs_USRKEz826j1VrY'  # corpsecretSecret是管理组凭证密钥
    accesstoken = gettoken(corpid, corpsecret)
    senddata(accesstoken, args.user, args.message)
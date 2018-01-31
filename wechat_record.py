author = '郑君'
'''
这个脚本意在处理你和特定朋友之间聊天记录的备份，且对关键字“打卡”进行特殊处理
'''

import itchat
import os, time, re, codecs
from itchat.content import *
itchat.auto_login(enableCmdQR = 2, hotReload = True)

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_send_test(msg):
    if not os.path.exists(r'./whole_chat'):
        os.makedirs(r'./whole_chat')
    if not os.path.exists(r'./daka_chat'):
        os.makedirs(r'./daka_chat')
    try:
        user = msg['User']
        remark_name = user['RemarkName']
        if remark_name != '备注':  # 此处应写你朋友的备注名，考虑到备注的更改自己是知情的，防止朋友修改微信名造成故障
            return
        nick_name = itchat.search_friends(userName = msg['FromUserName'])['NickName']
        text = msg['Text']
        res = nick_name + ':' + text
        with codecs.open(r'./whole_chat/' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.cht', 'a', 'utf-8') as f1:
            f1.write(time.strftime('%H-%M-%S@',time.localtime(time.time())) + res + '\n')
        if re.match('打卡', text):
            with codecs.open(r'./daka_chat/' + time.strftime('%Y-%W',time.localtime(time.time())) + '.cht', 'a', 'utf-8')as f2:
                f2.write(time.strftime('%Y-%m-%d@',time.localtime(time.time())) + res + '\n')
        # print(res)
    except KeyboardInterrupt:
        pass
if __name__ == '__main__':
    try:
        itchat.run()
    except KeyboardInterrupt:
        pass

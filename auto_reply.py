import itchat
import api


conf = api.TulingConf('2b902a5a9cb741abafd33928bfc0c536','3a20af4af4318431')
TBS = api.TulingService(conf)

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    myself = itchat.get_friends(update=True)[0]['NickName']
    content = msg['Content']
    friend = msg['User']['NickName']
    nickname,username = get_self_info()
    if friend != myself and friend!= 'FRIEND':
        print('%s: %s' % (friend, content))
        answer = TBS.get_answer(msg['Text'])
        if answer is None:
            if msg['FromUserName'] != username:
                itchat.send('功能完善中,请换个方式撩主人', msg['FromUserName'])
                print('我：%s' % answer)
        else:
            if msg['FromUserName'] != username:
                itchat.send(answer, msg['FromUserName'])
                print('我：%s' % answer)
            else:
                print('我：%s' % answer)
    else:
        itchat.send('你是猪', msg['FromUserName'])

def group_id(name):
    df = itchat.search_chatrooms(name=name)
    return df[0]['UserName']

def get_self_info():
    username = itchat.search_friends()
    return username['NickName'],username['UserName']

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_text_reply(msg):
    nickname,username = get_self_info()
    group_name = msg['User']['NickName']
    group = ['一支穿云箭 千军万马来相见', '全国远景x3交流群']
    group_info = itchat.search_chatrooms(name=group_name)
    item = group_info[0]['UserName']
    if group_name in group:
        if msg['FromUserName'] != username:
            itchat.send(TBS.get_answer(msg['Text']), item)
        else:
            print(msg['NickName'])


if __name__ == "__main__":
    itchat.auto_login(hotReload=True)
    itchat.run()
from flask import Flask, request
import telepot
import urllib3

proxy_url= "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url= proxy_url, num_pools=3,maxsize=10, retries = False, timeout= 30),
}

telepot.api._onetime_pool_spec =(urllib3.ProxyManager, dict(proxy_url= proxy_url, num_pools=1, maxsize=1,retries=False , timeout=30))
secret="bot"
bot = telepot.Bot('Token')
bot.setWebhook("https://reza3977.pythonanywhere.com/{}".format(secret), max_connections =1)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text= msg['text']
        if text == '/start':
            bot.sendMessage(chat_id,'send your messages.')
           # bot.sendMessage(chat_id,Ismember(chat_id))
           # x = open("members.txt", "a")
           # x.write(''.format(chat_id))
           # z = open("members.txt", "r")
           # bot.sendMessage(chat_id,z.read())
        elif text[0:4] == '/say':#chat with users 
                    if chat_id == admin_chat_id:
                        u_id=''
                        textlen=0
                        for i in text[5:20]:
                            textlen += 1
                            if i != '|':
                                u_id += i
                            if i == '|':
                                break
                        u_id=int(u_id)
                        bot.sendMessage(u_id,text[5 + textlen:])
                        bot.sendMessage('admin_chat_id',text[5 + textlen:]+"  was sent.")#for example admin send /say user_id |hi and bot send hi to user_id.
        bot.sendMessage('admin_chat_id',msg)
        mention="tg://openmessage?user_id={}".format(chat_id)
        bot.sendMessage('admin_chat_id',mention)
        bot.forwardMessage('admin_chat_id', msg['chat']['id'], msg['message_id'])
        bot.sendMessage(chat_id,"sent.")
    else:
        bot.forwardMessage('admin_chat_id', msg['chat']['id'], msg['message_id'])



app = Flask(__name__)

@app.route('/{}'.format(secret),methods = ["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update :
        handle(update['message'])
    return "ok"

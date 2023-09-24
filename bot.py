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
bot.setWebhook("domain{}".format(secret), max_connections =1)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text= msg['text']
        if text == '/start':
            bot.sendMessage(chat_id,'send your messages.')
        if chat_id == admin_chat_id:#reply messages
            try:
                bot.sendMessage(msg['reply_to_message']['forward_from']['id'],msg["text"])
                bot.sendMessage(chat_id,'sent')
            except KeyError : pass #For example, the admin replyes to a user message and sends hi, and the robot sends hi to the same user whose message was replyed.
        bot.sendMessage('admin_chat_id',msg)
        mention="tg://openmessage?user_id={}".format(chat_id)
        bot.sendMessage('admin_chat_id',mention)
        bot.forwardMessage('admin_chat_id', msg['chat']['id'], msg['message_id'])
        bot.sendMessage(chat_id,"sent.")
    else:
        bot.forwardMessage('admin_chat_id', msg['chat']['id'], msg['message_id'])
        bot.sendMessage(chat_id,"sent.")

app = Flask(__name__)


@app.route('/{}'.format(secret),methods = ["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update :
        handle(update['message'])
    return "ok"

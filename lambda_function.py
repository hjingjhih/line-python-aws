import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['YOUR_CHANNEL_SECRET'])

def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='在 AWS 的中心大聲呼喊：' + event.message.text))

    try:
        # get X-Line-Signature header value
        copy_headers = {key.lower(): value for key, value in event['headers'].items()}
        signature = copy_headers['x-line-signature']

        # get request body as text
        body = event['body']
        
        # handle webhook body
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        return {'statusCode': 400, 'body': 'InvalidSignature'}
        
    except Exception as e:
        print(e)
        return {'statusCode': 400, 'body': str(e)}

    return {'statusCode': 200, 'body': 'OK'}
    
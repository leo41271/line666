from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('o1xpYjoSdxrQgFHC4zptnsZN1R/meFs4zqwg9sThciduUL0v0QOu1TvkDf+B714bGzHye1HV1LtcODlW3qunvn/PDsKE7BHEBUj2P3HfXh1WsjrlMOIedTK2T//G8tiSARMWSd7z3+kTe78ig3xtNwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('5257c2cb1bc268e0dbbb65d09a911ef6')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
#github.com/54bp6cl6
#關鍵字系統
def KeyWord(event):
    KeyWordDict = {"你好":"你也好啊",
                   "你是誰":"我是大帥哥",
                   "帥":"帥炸了",
                   "差不多了":"讚!!!"}

    for k in KeyWordDict.keys():
        if event.message.text.find(k) != -1:
            return [True,KeyWordDict[k]]
    return [False]

#按鈕版面系統
def Button(event):
    return TemplateSendMessage(
        alt_text='特殊訊息，請進入手機查看',
        template=ButtonsTemplate(
            thumbnail_image_url='https://github.com/54bp6cl6/LineBotClass/blob/master/logo.jpg?raw=true',
            title='HPClub - Line Bot 教學',
            text='大家學會了ㄇ',
            actions=[
                PostbackTemplateAction(
                    label='還沒',
                    data='還沒'
                ),
                MessageTemplateAction(
                    label='差不多了',
                    text='差不多了'
                ),
                URITemplateAction(
                    label='幫我們按個讚',
                    uri='https://www.facebook.com/ShuHPclub'
                )
            ]
        )
    )

#回覆函式
def Reply(event):
    Ktemp = KeyWord(event)
    if Ktemp[0]:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = Ktemp[1]))
    else:
        line_bot_api.reply_message(event.reply_token,
            Button(event))

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Reply(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

#處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data.split(',')
    if command[0] == "還沒":
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="還沒就趕快練習去~~~"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

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
#lineBot+python 輕鬆建立聊天機器人
#https://developers.line.biz/en/reference/messaging-api/#wh-sticker     https://developers.line.biz/media/messaging-api/sticker_list.pdf      stiker List
#notepad++
#Sublime
#_______________________________________________________________________

#關鍵字系統
def Keyword(event):
    KeyWordDict = {"你好":["text","你也好啊"],
                   "你是誰":["text","我是大帥哥"],
                   "差不多了":["text","讚!!!"],
                   "帥":["sticker",'1','120']}

    for k in KeyWordDict.keys():
        if event.message.text.find(k) != -1:
            if KeyWordDict[k][0] == "text":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = KeyWordDict[k][1]))
            elif KeyWordDict[k][0] == "sticker":
                line_bot_api.reply_message(event.reply_token,StickerSendMessage(
                    package_id=KeyWordDict[k][1],
                    sticker_id=KeyWordDict[k][2]))
            return True
    return False

#按鈕版面系統
def Button(event):
    line_bot_api.reply_message(event.reply_token,
        TemplateSendMessage(
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
    )

#指令系統，若觸發指令會回傳True
def Command(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U95418ebc4fffefdd89088d6f9dabd75b":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
        return True
    else:
        return False

#回覆函式，指令 > 關鍵字 > 按鈕
def Reply(event):
    if not Command(event):
        if not Keyword(event):
            Button(event)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Reply(event)
        '''
        line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.source.user_id + "說:"))
        line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.message.text))
        '''
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
        
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id='1',
            sticker_id='410')
    )
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

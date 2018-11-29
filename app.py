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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

def Reply(text):
	if text =="h1" || text =="gg":
		return TextSendMessage(text = "hello")

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

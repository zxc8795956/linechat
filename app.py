from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('iPltUXR81NqwX/khG13NvGgSYI2N6DbiE/CYZcAqY2MV8iOiDR5bj3VR3QKRjO+0jTeXP/U3/1LuwiWaKIf54KTh1G8ehDWm5TbCSs6T2OQNi7Ia3TiNP9fyMKIxQ4lpINFLF1tg1Y4d0p/j9nX4FAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bc08cf4b2a9b82b97e540585a9a07b9c')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
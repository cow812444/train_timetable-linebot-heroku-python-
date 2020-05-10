from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import re
from datetime import (
  datetime, timedelta
)
import base64
import requests
import copy
from auth import Auth
from train_time_table import TrainTimeTable
from dict_menu import DictMenu

auth = Auth()
trainCrawler = TrainTimeTable()
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
# Channel Secret 
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET_ID'))
# Get Date
today_str = datetime.strftime(datetime.today(), '%Y-%m-%d')

#準備編輯flex msg
flexMsgModule = DictMenu.flexMsgModule
flexMsgModule_2 = DictMenu.flexMsgModule_2
location = DictMenu.location

#selenimu crawler set-up
#chrome_options = webdriver.ChromeOptions()
#chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--no-sandbox")
#driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        from_where = ''
        end_where = ''
        ipt_pattern = re.search(r'(基隆|三坑|八堵|七堵|百福|五堵|汐止|汐科|南港|松山|臺北|台北|台南|台中|萬華|板橋|浮洲|樹林|南樹林|山佳|鶯歌|桃園|內壢|中壢|埔心|楊梅|富岡|新富|北湖|湖口|新豐|竹北|北新竹|新竹|三姓橋|香山|崎頂|竹南|造橋|豐富|苗栗|南勢|銅鑼|三義|泰安|后里|豐原|栗林|潭子|頭家厝|松竹|太原|精武|臺中|五權|大慶|烏日|新烏日|成功|彰化|花壇|大村|員林|永靖|社頭|田中|二水|林內|石榴|斗六|斗南|石龜|大林|民雄|嘉北|嘉義|水上|南靖|後壁|新營|柳營|林鳳營|隆田|拔林|善化|南科|新市|永康|大橋|臺南|林森|南臺南|保安|仁德|中洲|大湖|路竹|岡山|橋頭|楠梓|新左營|左營|內惟|美術館|鼓山|三塊厝|高雄|民族|科工館|正義|鳳山|後庄|九曲堂|六塊厝|屏東).*[到去回](基隆|三坑|八堵|七堵|百福|五堵|汐止|汐科|南港|松山|臺北|台北|台南|台中|萬華|板橋|浮洲|樹林|南樹林|山佳|鶯歌|桃園|內壢|中壢|埔心|楊梅|富岡|新富|北湖|湖口|新豐|竹北|北新竹|新竹|三姓橋|香山|崎頂|竹南|造橋|豐富|苗栗|南勢|銅鑼|三義|泰安|后里|豐原|栗林|潭子|頭家厝|松竹|太原|精武|臺中|五權|大慶|烏日|新烏日|成功|彰化|花壇|大村|員林|永靖|社頭|田中|二水|林內|石榴|斗六|斗南|石龜|大林|民雄|嘉北|嘉義|水上|南靖|後壁|新營|柳營|林鳳營|隆田|拔林|善化|南科|新市|永康|大橋|臺南|林森|南臺南|保安|仁德|中洲|大湖|路竹|岡山|橋頭|楠梓|新左營|左營|內惟|美術館|鼓山|三塊厝|高雄|民族|科工館|正義|鳳山|後庄|九曲堂|六塊厝|屏東)', event.message.text)
        if ipt_pattern:
            from_where = ipt_pattern.group(1)
            end_where = ipt_pattern.group(2)
        if from_where != '' and end_where != '':
            flexMsgModule_2 = copy.deepcopy(flexMsgModule)
            flexMsgModule_2['body']['contents'][1]['text'] = from_where + ' → ' + end_where
            url = 'https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/DailyTrainTimetable/OD/{fr}/to/{ed}/{dates}?$count=true&$format=JSON'.format(fr=location[from_where], ed=location[end_where], dates=today_str)
            headers = {'algorithm': 'hmac-sha1', \
                        'headers': 'X-date', \
                        'content-type': 'application/json'
                        }
            headers.update(auth.get_auth_header())
            r = requests.get(url, timeout=float(10), headers=headers)
            r_obj = r.json()
            result_msg = trainCrawler.get_train_time_table(flexMsgModule_2, r_obj)
            flexMsgs = FlexSendMessage(alt_text='您的火車時刻表', contents=result_msg)
            line_bot_api.reply_message(event.reply_token, flexMsgs)
        else:
            msg = TextSendMessage(text='輸入格式錯誤！')
            line_bot_api.reply_message(event.reply_token, msg)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

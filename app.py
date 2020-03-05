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
from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from datetime import timedelta
from time import mktime
import base64
import requests
import copy

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
# Channel Secret 
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET_ID'))
# 台鐵 Access App_id token
app_id = os.environ.get('APP_ID')
# 台鐵 Access App_key token
app_key = os.environ.get('APP_KEY')

today = datetime.today()
today_str = datetime.strftime(today, '%Y-%m-%d')

#開啟json準備編輯flex msg
flexMsgModule = {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "您的火車時刻表",
          "weight": "bold",
          "color": "#1DB446",
          "size": "sm"
        },
        {
          "type": "text",
          "text": "桃園 → 竹北",
          "weight": "bold",
          "size": "xxl",
          "margin": "md"
        },
        {
          "type": "text",
          "text": "歷經 10 站",
          "size": "sm",
          "color": "#aaaaaa",
          "wrap": True
        },
        {
          "type": "separator",
          "margin": "xs"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "xxl",
          "spacing": "sm",
          "contents": [
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "出發時間",
                  "size": "xs",
                  "color": "#555555",
                  "align": "start",
                  "weight": "bold"
                },
                {
                  "type": "text",
                  "text": "抵達時間",
                  "size": "xs",
                  "color": "#555555",
                  "align": "start",
                  "weight": "bold"
                },
                {
                  "type": "text",
                  "text": "乘車時間",
                  "size": "xs",
                  "align": "start",
                  "color": "#555555",
                  "weight": "bold"
                },
                {
                  "type": "text",
                  "text": "車種編號",
                  "color": "#555555",
                  "size": "xs",
                  "align": "center",
                  "weight": "bold"
                }
              ]
            },
            {
              "type": "separator",
              "margin": "xs"
            }
          ]
        }
      ]
    },
    "styles": {
      "header": {
        "separator": False
      },
      "footer": {
        "separator": True
      }
    }
  }
timeTrainModule = {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "text",
        "text": "09:27",
        "size": "sm",
        "color": "#555555",
        "align": "center"
      },
      {
        "type": "text",
        "text": "10:14",
        "size": "sm",
        "color": "#555555",
        "align": "center"
      },
      {
        "type": "text",
        "text": "47分鐘",
        "size": "xxs",
        "color": "#555555",
        "align": "center"
      },
      {
        "type": "text",
        "text": "區間-1247",
        "size": "xxs",
        "color": "#555555",
        "align": "center"
      }
    ],
    "margin": "lg"
  }

location = {'基隆': '0900',
 '三坑': '0910',
 '八堵': '0920',
 '七堵': '0930',
 '百福': '0940',
 '五堵': '0950',
 '汐止': '0960',
 '汐科': '0970',
 '南港': '0980',
 '松山': '0990',
 '臺北': '1000',
 '台北': '1000',
 '萬華': '1010',
 '板橋': '1020',
 '浮洲': '1030',
 '樹林': '1040',
 '南樹林': '1050',
 '山佳': '1060',
 '鶯歌': '1070',
 '桃園': '1080',
 '內壢': '1090',
 '中壢': '1100',
 '埔心': '1110',
 '楊梅': '1120',
 '富岡': '1130',
 '新富': '1140',
 '北湖': '1150',
 '湖口': '1160',
 '新豐': '1170',
 '竹北': '1180',
 '北新竹': '1190',
 '新竹': '1210',
 '三姓橋': '1220',
 '香山': '1230',
 '崎頂': '1240',
 '竹南': '1250',
 '造橋': '3140',
 '豐富': '3150',
 '苗栗': '3160',
 '南勢': '3170',
 '銅鑼': '3180',
 '三義': '3190',
 '泰安': '3210',
 '后里': '3220',
 '豐原': '3230',
 '栗林': '3240',
 '潭子': '3250',
 '頭家厝': '3260',
 '松竹': '3270',
 '太原': '3280',
 '精武': '3290',
 '臺中': '3300',
 '台中': '3300',
 '五權': '3310',
 '大慶': '3320',
 '烏日': '3330',
 '新烏日': '3340',
 '成功': '3350',
 '彰化': '3360',
 '花壇': '3370',
 '大村': '3380',
 '員林': '3390',
 '永靖': '3400',
 '社頭': '3410',
 '田中': '3420',
 '二水': '3430',
 '林內': '3450',
 '石榴': '3460',
 '斗六': '3470',
 '斗南': '3480',
 '石龜': '3490',
 '大林': '4050',
 '民雄': '4060',
 '嘉北': '4070',
 '嘉義': '4080',
 '水上': '4090',
 '南靖': '4100',
 '後壁': '4110',
 '新營': '4120',
 '柳營': '4130',
 '林鳳營': '4140',
 '隆田': '4150',
 '拔林': '4160',
 '善化': '4170',
 '南科': '4180',
 '新市': '4190',
 '永康': '4200',
 '大橋': '4210',
 '臺南': '4220',
 '台南': '4220',
 '林森': '4230',
 '南臺南': '4240',
 '保安': '4250',
 '仁德': '4260',
 '中洲': '4270',
 '大湖': '4290',
 '路竹': '4300',
 '岡山': '4310',
 '橋頭': '4320',
 '楠梓': '4330',
 '新左營': '4340',
 '左營': '4350',
 '內惟': '4360',
 '美術館': '4370',
 '鼓山': '4380',
 '三塊厝': '4390',
 '高雄': '4400',
 '民族': '4410',
 '科工館': '4420',
 '正義': '4430',
 '鳳山': '4440',
 '後庄': '4450',
 '九曲堂': '4460',
 '六塊厝': '4470',
 '屏東': '5000'}

#selenimu crawler set-up
#chrome_options = webdriver.ChromeOptions()
#chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--no-sandbox")
#driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)

# 透過app_id & app_key計算hmac-sha1 key
class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

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
        ipt_pattern = re.search(r'(基隆|三坑|八堵|七堵|百福|五堵|汐止|汐科|南港|松山|臺北|萬華|板橋|浮洲|樹林|南樹林|山佳|鶯歌|桃園|內壢|中壢|埔心|楊梅|富岡|新富|北湖|湖口|新豐|竹北|北新竹|新竹|三姓橋|香山|崎頂|竹南|造橋|豐富|苗栗|南勢|銅鑼|三義|泰安|后里|豐原|栗林|潭子|頭家厝|松竹|太原|精武|臺中|五權|大慶|烏日|新烏日|成功|彰化|花壇|大村|員林|永靖|社頭|田中|二水|林內|石榴|斗六|斗南|石龜|大林|民雄|嘉北|嘉義|水上|南靖|後壁|新營|柳營|林鳳營|隆田|拔林|善化|南科|新市|永康|大橋|臺南|林森|南臺南|保安|仁德|中洲|大湖|路竹|岡山|橋頭|楠梓|新左營|左營|內惟|美術館|鼓山|三塊厝|高雄|民族|科工館|正義|鳳山|後庄|九曲堂|六塊厝|屏東).*[到去回](基隆|三坑|八堵|七堵|百福|五堵|汐止|汐科|南港|松山|臺北|萬華|板橋|浮洲|樹林|南樹林|山佳|鶯歌|桃園|內壢|中壢|埔心|楊梅|富岡|新富|北湖|湖口|新豐|竹北|北新竹|新竹|三姓橋|香山|崎頂|竹南|造橋|豐富|苗栗|南勢|銅鑼|三義|泰安|后里|豐原|栗林|潭子|頭家厝|松竹|太原|精武|臺中|五權|大慶|烏日|新烏日|成功|彰化|花壇|大村|員林|永靖|社頭|田中|二水|林內|石榴|斗六|斗南|石龜|大林|民雄|嘉北|嘉義|水上|南靖|後壁|新營|柳營|林鳳營|隆田|拔林|善化|南科|新市|永康|大橋|臺南|林森|南臺南|保安|仁德|中洲|大湖|路竹|岡山|橋頭|楠梓|新左營|左營|內惟|美術館|鼓山|三塊厝|高雄|民族|科工館|正義|鳳山|後庄|九曲堂|六塊厝|屏東)', event.message.text)
        if ipt_pattern:
            from_where = ipt_pattern.group(1)
            end_where = ipt_pattern.group(2)
        if from_where != '' and end_where != '':
            flexMsgModule['body']['contents'][1]['text'] = from_where + ' → ' + end_where
            #print(location[from_where])
            #print(location[end_where])
            app = Auth(app_id, app_key)
            url = 'https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/DailyTrainTimetable/OD/{fr}/to/{ed}/{dates}?$count=true&$format=JSON'.format(fr=location[from_where], ed=location[end_where], dates=today_str)
            headers = {'algorithm': 'hmac-sha1', \
                        'headers': 'X-date', \
                        'content-type': 'application/json'
                        }
            headers.update(app.get_auth_header())
            r = requests.get(url, timeout=float(10), headers=headers)
            r_obj = r.json()
            result_msg = get_train_time_table(r_obj)
            #msg = TextSendMessage(text=result_msg)
            line_bot_api.reply_message(event.reply_token, result_msg)
            #print(r_obj['Count'])
        else:
            msg = TextSendMessage(text='輸入格式錯誤！')
            line_bot_api.reply_message(event.reply_token, msg)
        #message = TextSendMessage(text=event.message.text)
        #line_bot_api.reply_message(event.reply_token, message)

def get_train_time_table(r_obj):
    trainTimeTable = {}
    timeSequence = []

    #get now time (datetime format)
    nowTime = datetime.strftime(datetime.now()- timedelta(days=43869), '%H:%M')
    print('目前時間: ', nowTime)
    #print(datetime.now()- timedelta(days=43893))
    print('---')
    if str(r_obj['Count']) == '0':
        return '查無航班'

    for payload in r_obj['TrainTimetables']:
        #set default information
        trainNo = payload['TrainInfo']['TrainNo']
        trainType = payload['TrainInfo']['TrainTypeName']['Zh_tw']
        startStation = payload['StopTimes'][0]['StationName']['Zh_tw']
        arrivalStation = payload['StopTimes'][1]['StationName']['Zh_tw']
        startTime_str = payload['StopTimes'][0]['ArrivalTime']
        arrivalTime_str = payload['StopTimes'][1]['DepartureTime']
        stopSequence_int = payload['StopTimes'][1]['StopSequence'] - payload['StopTimes'][0]['StopSequence']
        

        #判斷時間順序
        regconizeTime = startTime_str.replace(':', '')
        
        #string to datetime format
        startTime_dt = datetime.strptime(startTime_str, '%H:%M')
        arrivalTime_dt = datetime.strptime(arrivalTime_str, '%H:%M')

        #計算行駛時間並判定車趟行駛與否
        duration = []
        duration_dt =  arrivalTime_dt - startTime_dt
        duration_str = str(duration_dt).split(':')
        if duration_str[0] != '0':
            duration.append(duration_str[0]+'小時')
        duration.append(duration_str[1]+'分鐘')
        duration = ''.join(duration)
        checktime = str(startTime_dt - datetime.now() + timedelta(days=43893))
        check = re.search(r'-1 day', checktime)

        #將當日未行駛車趟放入dict
        if not check:
            timeSequence.append(regconizeTime)
            appends = {
                regconizeTime:[trainNo, trainType, startStation, arrivalStation, startTime_str, arrivalTime_str]
                }
            trainTimeTable.update(appends)
            
    #對所有車趟進行時間排序
    timeSequence.sort()
    resultList = []
    #timeTrainModule_2 = copy.deepcopy(timeTrainModule)
    flexMsgModule['body']['contents'][2]['text'] = '歷經 ' + str(stopSequence_int) + ' 站'
    for trainInfo in timeSequence:
        #print(trainTimeTable[trainInfo])
        timeTrainModule_2 = copy.deepcopy(timeTrainModule)
        timeTrainModule_2['contents'][0]['text'] = trainTimeTable[trainInfo][4]
        timeTrainModule_2['contents'][1]['text'] = trainTimeTable[trainInfo][5]
        timeTrainModule_2['contents'][2]['text'] = duration
        timeTrainModule_2['contents'][3]['text'] = trainTimeTable[trainInfo][1] + '-' + trainTimeTable[trainInfo][0]
        flexMsgModule['body']['contents'][4]['contents'].append(timeTrainModule_2)
        result = '從 {from_}-{from_time} 到 {end}-{end_time} ({type}-{No})\r\n'.format(
            type=trainTimeTable[trainInfo][1], No=trainTimeTable[trainInfo][0],
            from_=trainTimeTable[trainInfo][2], end=trainTimeTable[trainInfo][3], 
            from_time=trainTimeTable[trainInfo][4], end_time=trainTimeTable[trainInfo][5])
        #msg = TextSendMessage(text=result)
        #line_bot_api.reply_message(event.reply_token, msg)
        resultList.append(result)
    #msg = TextSendMessage(text=''.join(resultList))
    flexMsg = FlexSendMessage(alt_text='您的火車時刻表', contents=flexMsgModule)
    return flexMsg
        #print('{type}({No})'.format(type=trainType, No=trainNo))
        #print('從 {from_}-{from_time} 到 {end}-{end_time}'.format(
        #    from_=startStation, end=arrivalStation, 
        #    from_time=startTime_str, end_time=arrivalTime_str))
        #print('耗時: ', duration_dt)
        #print('---')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

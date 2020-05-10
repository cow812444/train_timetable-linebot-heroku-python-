from dict_menu import DictMenu
from datetime import (
  datetime, timedelta
)
import re
import copy
import requests
from auth import Auth
from dict_menu import DictMenu

class TrainTimeTable:

    def call_train_station_api(self, from_where, end_where):
        auth = Auth()
        flexMsgModule = DictMenu.flexMsgModule
        location = DictMenu.location
        today_str = datetime.strftime(datetime.today(), '%Y-%m-%d')
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
            return r_obj,flexMsgModule_2

    def get_train_time_table(self, flexMsg, r_obj):
        trainTimeDict = DictMenu.timeTrainModule
        trainTimeTable = {}
        timeSequence = []

        #get now time (datetime format)
        nowTime = datetime.strftime(datetime.now()- timedelta(days=43869), '%H:%M')
        print('目前時間: ', nowTime)
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
            dt = datetime.today()-datetime.strptime("1900-1-1", "%Y-%m-%d")
            checktime = str(startTime_dt - datetime.now() + timedelta(days=dt.days))
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
        flexMsg['body']['contents'][2]['text'] = '歷經 ' + str(stopSequence_int) + ' 站'
        for trainInfo in timeSequence:
            timeTrainModule_2 = copy.deepcopy(trainTimeDict)
            timeTrainModule_2['contents'][0]['text'] = trainTimeTable[trainInfo][4]
            timeTrainModule_2['contents'][1]['text'] = trainTimeTable[trainInfo][5]
            timeTrainModule_2['contents'][2]['text'] = duration
            timeTrainModule_2['contents'][3]['text'] = trainTimeTable[trainInfo][1] + '-' + trainTimeTable[trainInfo][0]
            flexMsg['body']['contents'][4]['contents'].append(timeTrainModule_2)
            result = '從 {from_}-{from_time} 到 {end}-{end_time} ({type}-{No})\r\n'.format(
                type=trainTimeTable[trainInfo][1], No=trainTimeTable[trainInfo][0],
                from_=trainTimeTable[trainInfo][2], end=trainTimeTable[trainInfo][3], 
                from_time=trainTimeTable[trainInfo][4], end_time=trainTimeTable[trainInfo][5])
            resultList.append(result)
        return flexMsg
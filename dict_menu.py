class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DictMenu(metaclass=Singleton):
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
    flexMsgModule_2 = {}
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

    rich_menu_tech_support = {
    "type": "carousel",
    "contents": [
        {
        "type": "bubble",
        "size": "micro",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "VCA虛擬客戶助理",
                "weight": "bold",
                "size": "sm",
                "wrap": true
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "text",
                    "text": "5.0",
                    "size": "xs",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "智能客服信用卡助手查帳產品/業務查詢業務辦理中樞平臺 基於自然語言理解、情感計算、深度學習技術，為企業客戶提供從客戶服務、業務辦理、到諮詢等在內的全方位客戶虛擬助理。",
                        "wrap": true,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "VEA虛擬企業助理",
                "weight": "bold",
                "size": "sm",
                "wrap": true
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                },
                {
                    "type": "text",
                    "text": "4.0",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "以AI對話機器人為核心，通過自然語言人機對話，為企業內部行政、人事、財務、IT部門提供涵蓋企業政策諮詢、年假及福利管理、員工關系維護等領域的企業虛擬助理。",
                        "wrap": true,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "micro",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "多模態交互系統",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                },
                {
                    "type": "icon",
                    "size": "xs",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                },
                {
                    "type": "text",
                    "text": "MAX",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "通過軟硬一體的終端設備及系統服務，並融合竹間的計算機視覺理解、情感情緒識別和中文自然語言理解及竹間獨創的“多模態情感識別模型”等技術，打造AI+新零售、AI+教育及AI+出行等領域產品。",
                        "wrap": true,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        }
    ]
    }
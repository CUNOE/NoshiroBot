import os
DOG_TAG = True
SHIP_PREVIEW = True
POST_ID = True  # 测试用，默认请改为True
REQUEST_TIMEOUT = 10
LAST_CW_MUNBER = '21'  # 最新赛季cw
BOT_VERSON = 'KokomiBot 3.2.6 @Maoyu'
API_URL = 'http://www.wows-coral.com:443'  # 默认数据接口
API_TOKEN = 'kokomi'
PLATFORM = 'qq'
PIC_TYPE = 'base64'  # 发送图片使用的协议（base64/file），qq平台请使用base64
# 如果图片类型为file则需要配置,默认为上一目录中的temp文件
PIC_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')

import os
import httpx
import time
import datetime
import cv2
import numpy as np
from PIL import Image
import gc
from httpx import (
    TimeoutException,
    ConnectTimeout,
    ReadTimeout
)
from .config import (
    REQUEST_TIMEOUT,
    API_URL,
    API_TOKEN,
    PIC_TYPE,
    BOT_VERSON
)
from .data_source import (
    img_to_b64,
    img_to_file,
    x_coord,
    add_text
)
from .data_source import (
    font_list,
    server_table_list
)
import logging
file_path = os.path.dirname(__file__)
# 配置日志输出到文件
logging.basicConfig(filename=os.path.join(
    file_path, 'log', 'error.log'), level=logging.ERROR)


def int_to_str(num: int):
    str_num = str(num)
    if len(str_num) > 3:
        return str_num[:len(str_num)-3] + ' ' + str_num[len(str_num)-3:]
    else:
        return str_num


def main(
    result
):
    text_list = []
    fontStyle = font_list[1][55]
    t = 0
    for type_index in ['now', 'avg', 'max', 'min']:
        s = 0
        for server_index in ['asia', 'eu', 'na', 'ru', 'cn']:
            if server_index in ['ru', 'cn']:
                str_number = '-'
            else:
                str_number = int_to_str(
                    result['data'][type_index][server_index])
            w = x_coord(str_number, fontStyle)
            text_list.append([(731.6-w/2+320*s, 704+115*t),
                             str_number, (0, 0, 0), 1, 55])
            s += 1
        t += 1

    res_img = cv2.imread(os.path.join(
        file_path, 'png', 'background', 'wws_server_1.png'), cv2.IMREAD_UNCHANGED)
    now_hour = datetime.datetime.now().hour
    if now_hour == 23:
        now_hour = 0
        date_str = time.strftime(
            "%Y-%m-%d", time.localtime(time.time()))  # 替换为你的日期，格式为 "年-月-日"
        time_str = "23:59:59"  # 替换为你的时间，格式为 "时:分:秒"
        dt = datetime.datetime.strptime(
            date_str + ' ' + time_str, "%Y-%m-%d %H:%M:%S")
        end_time = dt.timestamp()
    else:
        now_hour = now_hour + 1
        date_str = time.strftime(
            "%Y-%m-%d", time.localtime(time.time()))  # 替换为你的日期，格式为 "年-月-日"
        time_str = "{}:00:00".format(
            f'0{now_hour}' if now_hour < 10 else f'{now_hour}')  # 替换为你的时间，格式为 "时:分:秒"
        dt = datetime.datetime.strptime(
            date_str + ' ' + time_str, "%Y-%m-%d %H:%M:%S")
        end_time = dt.timestamp()
    hour_list = []
    i = 0
    while i <= 23:
        if now_hour == 0:
            hour_list.append(now_hour)
            now_hour = 23
        else:
            hour_list.append(now_hour)
            now_hour -= 1
        i += 1

    hour_list.reverse()
    max_member = []
    for server_index in ['asia', 'eu', 'na']:
        max_member.append(result['data']['max'][server_index])
    max_member = max(max_member)
    y_list = []
    for y_index in server_table_list:
        if y_index[0] < max_member:
            continue
        y_max = y_index[0]
        while y_max >= 0:
            y_list.append(y_max)
            y_max -= y_index[1]
        break
    fontStyle = font_list[1][25]
    i = 0
    for index in hour_list:
        w = x_coord(str(index), fontStyle)
        text_list.append(
            [(285-w/2+83*i, 2177), str(index), (84, 84, 84), 1, 25])
        i += 1
    i = 0
    for index in y_list:
        w = x_coord(str(index), fontStyle)
        text_list.append([(188-w, 1447+70*i), str(index), (84, 84, 84), 1, 25])
        i += 1

    for server_index in ['asia', 'eu', 'na']:
        asix_list = []
        for record_time, record_data in result['data']['server'][server_index].items():
            time_diff = end_time-int(record_time)
            x = 2194 - (1992*time_diff)/(24*60*60)
            y = 1456 + (700/y_list[0])*(y_list[0] - record_data)
            if x < 202:
                continue
            asix_list.append((int(x), int(y)))
        i = 0
        color_server = {
            'asia': (254, 182, 77),
            'eu': (91, 196, 159),
            'na': (50, 211, 235)
        }
        points = np.array(asix_list, np.int32)
        cv2.polylines(res_img, [points], isClosed=False,
                      color=color_server[server_index], thickness=10)
    now_time = '统计时间：'+time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    text_list.append(
        [(1700, 2237), now_time, (174, 174, 174), 1, 35])
    # Mat 转 ImageDraw
    if (isinstance(res_img, np.ndarray)):
        res_img = Image.fromarray(
            cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB))

    fontStyle = font_list[1][80]
    w = x_coord(BOT_VERSON, fontStyle)
    text_list.append(
        [(1214-w/2, 2316), BOT_VERSON, (174, 174, 174), 1, 80])
    res_img = add_text(text_list, res_img)
    res_img = res_img.resize((1214, 1273))
    return res_img


async def get_png(
    parameter: list,
):
    parameter = ['1']
    try:
        async with httpx.AsyncClient() as client:
            url = API_URL + '/server/active/' + f'?token={API_TOKEN}'
            res = await client.get(url, timeout=REQUEST_TIMEOUT)
            requset_code = res.status_code
            result = res.json()
            if requset_code == 200:
                pass
            else:
                return {'status': 'info', 'message': '数据接口请求失败'}
        if result['status'] != 'ok':
            return result
        res_img = main(
            result=result
        )
        res = {'status': 'ok', 'message': 'SUCCESS', 'img': None}
        if PIC_TYPE == 'base64':
            res['img'] = img_to_b64(res_img)
        elif PIC_TYPE == 'file':
            res['img'] = img_to_file(res_img)
        else:
            return {'status': 'error', 'message': '程序内部错误', 'error': 'PIC_TYPE 配置错误!'}
        del res_img
        gc.collect()
        return res
    except (TimeoutException, ConnectTimeout, ReadTimeout):
        return {'status': 'info', 'message': '网络请求超时,请稍后重试'}
    except Exception as e:
        logging.exception(
            f"Time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}, Parameter:{parameter}")
        return {'status': 'error', 'message': f'程序内部错误', 'error': str(type(e))}

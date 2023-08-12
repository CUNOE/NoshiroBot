import time
import os
import json
import re
import datetime
from .data_source import (
    tier_dict,
    type_dict,
    nation_dict,
    server_dict,
    a_tier_dict
)
from .scripts import (
    wws_basic,
    wws_bind,
    wws_rank,
    wws_recent,
    wws_search,
    wws_ship_rank,
    wws_server_rank,
    wws_select,
    wws_ship,
    wws_help,
    wws_roll,
    wws_clan_info,
    wws_clan_season,
    wws_clan_season_all,
    wws_group_rank,
    wws_server_1,
    wws_sx,
    wws_uid
)
from .scripts.config import PLATFORM, LAST_CW_MUNBER

debug = False
user = ['1111', '2023903210', 'asia', True, False, None]

file_path = os.path.dirname(__file__)


class select_funtion():
    async def main(
        message: list,
        user_id: str,
        group_id: str,
        group_name: str,
        group_data: dict
    ):
        result = {
            'status': 'ok',
            'message': 'SUCCESS',
            'function': None,
            'parameter': None
        }
        # wws help
        if message[1] == 'help' and len(message) == 2:
            result['function'] = wws_help.get_help_msg
            result['parameter'] = None
            return result
        '''
        用户基础数据功能
        '''
        if (
            message[1] == 'me' or
            (
                # qq平台 [CQ:at,qq=ID]
                message[1].startswith('[CQ:at,qq=') and
                message[1].endswith(']')
            ) or
            (
                # kook平台 (met)ID(met)
                message[1].startswith('(met)') and
                message[1].endswith('(met)')
            ) or
            (
                # discord平台  <@ID>'
                message[1].startswith('<@') and
                message[1].endswith('>')
            )
        ):
            # id获取
            if message[1] == 'me':
                user_id = user_id
            else:
                user_id = (re.findall(r'\d+', message[1]))[0]
            # 检查是否绑定
            if debug:
                uid = {'status': 'ok', 'message': 'SUCCESS', 'data': user}
            else:
                uid = await source.get_user_uid(user_id)
            if uid['status'] != 'ok':
                return uid
            else:
                uid = uid['data']
            # wws [me/@]
            if len(message) == 2:
                result['function'] = wws_basic.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    False if uid[3] == 0 else True,
                    False if uid[4] == 0 else True,
                    uid[5]
                ]
                return result
            # wws [me/@] 扫雪/sx
            elif message[2] in ['sx', '扫雪'] and len(message) == 3:
                result['function'] = wws_sx.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    False if uid[4] == 0 else True,
                    uid[5]
                ]
                return result
            # wws [me/@] rank
            elif message[2] == 'rank' and len(message) == 3:
                result['function'] = wws_rank.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    False if uid[3] == 0 else True,
                    False if uid[4] == 0 else True,
                    uid[5]
                ]
                return result
            # wws [me/@] rank recent [num]
            elif message[2] == 'rank' and message[3] == 'recent' and len(message) <= 5:
                if len(message) == 4:
                    date_num = 1
                else:
                    try:
                        date_num = int(message[4])
                    except:
                        result['status'] = 'info'
                        result['message'] = '输入的参数有误'
                        return result
                if datetime.datetime.now().hour in [0, 1, 2, 3, 4]:
                    add_date = 1
                else:
                    add_date = 0
                result['function'] = wws_recent.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    time.strftime(
                        "%Y-%m-%d", time.localtime(time.time()-24*60*60*date_num-24*60*60*add_date)),
                    time.strftime("%Y-%m-%d", time.localtime(time.time())),
                    'rank',
                    False if uid[3] == 0 else True,
                    False if uid[4] == 0 else True,
                    uid[5]
                ]
                return result
            # wws [me/@] recent [num]
            elif message[2] == 'recent' and len(message) <= 4:
                if len(message) == 3:
                    date_num = 1
                else:
                    try:
                        date_num = int(message[3])
                    except:
                        result['status'] = 'info'
                        result['message'] = '输入的参数有误'
                        return result
                if datetime.datetime.now().hour in [0, 1, 2, 3, 4]:
                    add_date = 1
                else:
                    add_date = 0
                result['function'] = wws_recent.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    time.strftime(
                        "%Y-%m-%d", time.localtime(time.time()-24*60*60*date_num-24*60*60*add_date)),
                    time.strftime("%Y-%m-%d", time.localtime(time.time())),
                    'pvp',
                    False if uid[3] == 0 else True,
                    False if uid[4] == 0 else True,
                    uid[5]
                ]
                return result
            # wws [me/@] ship rank [ship_name]
            elif message[2] == 'ship' and message[3] == 'rank' and len(message) == 5:
                ship_name = message[4]
                ship_id = seach.get_ship_id(ship_name=ship_name)
                if ship_id == None:
                    result['status'] = 'info'
                    result['message'] = '输入的船名有误'
                    return result
                result['function'] = wws_ship_rank.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    ship_id,
                    seach.get_ship_name(ship_id=ship_id)
                ]
                return result
            # wws [me/@] ship [ship_name]
            elif message[2] == 'ship' and len(message) == 4:
                ship_name = message[3]
                ship_id = seach.get_ship_id(ship_name=ship_name)
                if ship_id == None:
                    result['status'] = 'info'
                    result['message'] = '输入的船名有误'
                    return result
                result['function'] = wws_ship.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    ship_id,
                    seach.get_ship_name(ship_id=ship_id),
                    False if uid[3] == 0 else True,
                    False if uid[4] == 0 else True,
                    uid[5]
                ]
                return result
            # wws [me/@] ships [select1] ...
            elif message[2] == 'ships' and len(message) >= 4:
                select_list = message[3:]
                select_data = source.get_type(select_list)
                if select_data == None:
                    result['status'] = 'info'
                    result['message'] = '输入的参数有误'
                    return result
                result['function'] = wws_select.get_png
                result['parameter'] = [
                    uid[1],
                    uid[2],
                    select_data,
                    False if uid[3] == 0 else True,
                    False if uid[4] == 0 else True,
                    uid[5]
                ]
                return result
            # wws [me/@] clan
            elif message[2] == 'clan' and len(message) == 3:
                clan_data = await source.get_user_clan(aid=uid[1], server=uid[2])
                if clan_data['status'] != 'ok':
                    return clan_data
                result['function'] = wws_clan_info.get_png
                result['parameter'] = [
                    clan_data['data'],
                    uid[2]
                ]
                return result
            # wws [me/@] clan season
            elif message[2] == 'clan' and message[3] == 'season' and len(message) <= 5:
                clan_data = await source.get_user_clan(aid=uid[1], server=uid[2])
                if clan_data['status'] != 'ok':
                    return clan_data
                if len(message) == 4:
                    result['function'] = wws_clan_season.get_png
                    result['parameter'] = [
                        clan_data['data'],
                        LAST_CW_MUNBER,
                        uid[2]
                    ]
                    return result
                elif message[4] == 'all':
                    result['function'] = wws_clan_season_all.get_png
                    result['parameter'] = [
                        clan_data['data'],
                        LAST_CW_MUNBER,
                        uid[2]
                    ]
                    return result
                else:
                    try:
                        cvc_season = int(message[4])
                        if cvc_season > 21 and cvc_season < 1:
                            result['status'] = 'info'
                            result['message'] = '输入的参数有误'
                            return result
                    except:
                        result['status'] = 'info'
                        result['message'] = '输入的参数有误'
                        return result
                    result['function'] = wws_clan_season.get_png
                    result['parameter'] = [
                        clan_data['data'],
                        str(cvc_season),
                        uid[2]
                    ]
                    return result
        '''
        Part 2 服务器
        '''
        if message[1].lower() in server_dict:
            server = server_dict[message[1].lower()]
            if len(message) == 3:
                uid = await source.get_user_id(name=message[2], server=server)
                if uid['status'] != 'ok':
                    return uid
                else:
                    uid = uid['data']
                result['function'] = wws_basic.get_png
                result['parameter'] = [
                    uid,
                    server,
                    True,
                    False,
                    None
                ]
                return result
            elif message[2] == 'set':
                result['function'] = wws_bind.main
                result['parameter'] = [
                    user_id,
                    server,
                    ''.join(message[3:]),
                    PLATFORM
                ]
                return result
            # wws server ship rank ship_name
            elif message[2] == 'ship' and message[3] == 'rank' and len(message) == 5:
                ship_name = message[4]
                ship_id = seach.get_ship_id(ship_name=ship_name)
                if ship_id == None:
                    result['status'] = 'info'
                    result['message'] = '输入的船名有误'
                    return result
                result['function'] = wws_server_rank.get_png
                result['parameter'] = [
                    server,
                    ship_id,
                    seach.get_ship_name(ship_id=ship_id)
                ]
                return result
             # wws id clan
            elif message[3] == 'clan' and len(message) == 4:
                clan_data = await source.get_clan_id(clan_name=message[2], server=server)
                if clan_data['status'] != 'ok':
                    return clan_data
                result['function'] = wws_clan_info.get_png
                result['parameter'] = [
                    clan_data['data'],
                    server
                ]
                return result
            # wws id clan season
            elif message[3] == 'clan' and message[4] == 'season' and len(message) <= 6:
                clan_data = await source.get_clan_id(clan_name=message[2], server=server)
                if clan_data['status'] != 'ok':
                    return clan_data
                if len(message) == 5:
                    result['function'] = wws_clan_season.get_png
                    result['parameter'] = [
                        clan_data['data'],
                        LAST_CW_MUNBER,
                        server
                    ]
                    return result
                elif message[5] == 'all':
                    result['function'] = wws_clan_season_all.get_png
                    result['parameter'] = [
                        clan_data['data'],
                        LAST_CW_MUNBER,
                        server
                    ]
                    return result
                else:
                    try:
                        cvc_season = int(message[5])
                        if cvc_season > 21 and cvc_season < 1:
                            result['status'] = 'info'
                            result['message'] = '输入的参数有误'
                            return result
                    except:
                        result['status'] = 'info'
                        result['message'] = '输入的参数有误'
                        return result
                    result['function'] = wws_clan_season.get_png
                    result['parameter'] = [
                        clan_data['data'],
                        str(cvc_season),
                        server
                    ]
                    return result

        '''
        '''
        if message[1] == 'roll' and len(message) >= 3:
            uid = await source.get_user_uid(user_id)
            if uid['status'] != 'ok':
                return uid
            else:
                uid = uid['data']
            select_list = message[2:]
            select_data = source.get_type(select_list)
            if select_data == None:
                result['status'] = 'info'
                result['message'] = '输入的参数有误'
                return result
            result['function'] = wws_roll.get_png
            result['parameter'] = [
                uid[1],
                uid[2],
                select_data,
                False if uid[3] == 0 else True,
                False if uid[4] == 0 else True,
                uid[5]
            ]
            return result
        # elif message[1] == 'server' and message[2] == '1' and len(message) == 3:
        #     result['function'] = wws_server_1.get_png
        #     result['parameter'] = None
        #     return result
        elif message[1] == 'bind' and len(message) == 3:
            if message[2].isdigit():
                result['function'] = wws_uid.main
                result['parameter'] = [
                    user_id,
                    message[2],
                    PLATFORM
                ]
                return result
            else:
                result['status'] = 'info'
                result['message'] = 'uid格式有误'
                return result
        elif message[1] == 'group' and message[2] == 'ship' and message[3] == 'rank' and len(message) == 5:
            if PLATFORM != 'qq':
                result['status'] = 'info'
                result['message'] = '当前平台不支持'
                return result
            ship_name = message[4]
            ship_id = seach.get_ship_id(ship_name=ship_name)
            if ship_id == None:
                result['status'] = 'info'
                result['message'] = '输入的船名有误'
                return result
            result['function'] = wws_group_rank.get_png
            result['parameter'] = [
                ship_id,
                seach.get_ship_name(ship_id=ship_id),
                group_id,
                group_name,
                group_data,
                None
            ]
            return result
        elif message[1] == 'me' and message[2] == 'group' and message[3] == 'ship' and message[4] == 'rank' and len(message) == 6:
            if PLATFORM != 'qq':
                result['status'] = 'info'
                result['message'] = '当前平台不支持'
                return result
            ship_name = message[5]
            ship_id = seach.get_ship_id(ship_name=ship_name)
            if ship_id == None:
                result['status'] = 'info'
                result['message'] = '输入的船名有误'
                return result
            result['function'] = wws_group_rank.get_png
            result['parameter'] = [
                ship_id,
                seach.get_ship_name(ship_id=ship_id),
                group_id,
                group_name,
                group_data,
                user_id
            ]
            return result
        return {
            'status': 'default',
            'message': '功能未开放',
            'function': None,
            'parameter': None
        }


class source:
    async def get_user_uid(user_id: str):
        # 从数据库获取绑定信息
        data = await wws_search.search_id(
            user_id=user_id,
            platform=PLATFORM
        )
        return data

    async def get_user_clan(aid: str, server: str):
        data = await wws_search.search_clan(
            aid=aid,
            server=server
        )
        return data

    async def get_user_id(name, server):
        data = await wws_search.search_user_id(
            name=name,
            server=server
        )
        return data

    async def get_clan_id(clan_name, server):
        data = await wws_search.search_clan_id(
            clan_name=clan_name,
            server=server
        )
        return data

    def get_type(info_message: list):
        info_tier = []
        info_type = []
        info_nation = []
        for index in info_message:
            if index == '':
                continue
            index = index.upper()
            # 依次判断输入的参数是否属于tier type nation中
            if index in tier_dict:
                info_tier.append(tier_dict[index])
                continue
            if index in type_dict:
                info_type.append(type_dict[index])
                continue
            if index in nation_dict:
                info_nation.append(nation_dict[index])
                continue
            # 参数均不属于tier type nation中，则判定非法参数
            return None
        return [info_tier, info_type, info_nation]


class seach:
    def get_ship_id(ship_name):
        ship_name_file_path = os.path.join(file_path, 'json', 'ship_name.json')
        temp = open(ship_name_file_path, "r", encoding="utf-8")
        ship_name_data = json.load(temp)
        temp.close()
        ship_name = seach.name_format(ship_name)
        return_dict = None
        for ship_id, ship_data in ship_name_data.items():
            if ship_name in ship_data['ship_name']['other']:
                return_dict = ship_id
        return return_dict

    def get_ship_name(ship_id):
        ship_name_file_path = os.path.join(file_path, 'json', 'ship_name.json')
        temp = open(ship_name_file_path, "r", encoding="utf-8")
        ship_name_data = json.load(temp)
        temp.close()
        ship_name = a_tier_dict[ship_name_data[ship_id]['tier']
                                ]+'    '+ship_name_data[ship_id]['ship_name']['zh_sg']
        return ship_name

    def name_format(in_str: str):
        in_str_list = in_str.split()
        in_str = None
        in_str = ''.join(in_str_list)
        en_list = {
            'a': ['à', 'á', 'â', 'ã', 'ä', 'å'],
            'e': ['è', 'é', 'ê', 'ë'],
            'i': ['ì', 'í', 'î', 'ï'],
            'o': ['ó', 'ö', 'ô', 'õ', 'ò', 'ō'],
            'u': ['ü', 'û', 'ú', 'ù', 'ū'],
            'y': ['ÿ', 'ý']
        }
        for en, lar in en_list.items():
            for index in lar:
                if index in in_str:
                    in_str = in_str.replace(index, en)
                if index.upper() in in_str:
                    in_str = in_str.replace(index.upper(), en.upper())
        re_str = ['_', '-', '·', '.', '\'']
        for index in re_str:
            if index in in_str:
                in_str = in_str.replace(index, '')
        in_str = in_str.lower()
        return in_str

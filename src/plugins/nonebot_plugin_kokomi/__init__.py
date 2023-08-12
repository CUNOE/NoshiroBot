import traceback
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.log import logger


from .command_select import select_funtion

__plugin_name__ = "nonebot_plugin_kokomi"
__plugin_des__ = "战舰世界水表机器人"
__plugin_author__ = "Maoyu <3197206779@qq.com>"
__plugin_version__ = "3.2.0"

debug = False
superuser = ''
wws_bot = on_startswith("wws")


def group_data_formate(group_data: dict):
    processed_data = {}
    for group_member in group_data:
        processed_data[group_member['user_id']] = group_member['nickname']
    return processed_data


@wws_bot.handle()
async def main(bot: Bot, ev: MessageEvent):
    try:
        session_id = str(ev.get_session_id())
        if 'group' in session_id:
            split_id = session_id.split('_')
            qq_id = split_id[2]
            gruop_id = split_id[1]
        else:
            qq_id = session_id
            gruop_id = None
        group_name = 'None'
        group_data = None
        split_msg = str(ev.message).split()
        if len(split_msg) == 1:
            await wws_bot.finish()
        if gruop_id != None and 'group' in split_msg:
            group_data = await bot.get_group_member_list(group_id=gruop_id)
            group_data = group_data_formate(group_data)
            group_info = await bot.get_group_list()
            for index in group_info:
                if str(index['group_id']) == gruop_id:
                    group_name = index['group_name']
                else:
                    continue
        fun = await select_funtion.main(
            message=split_msg,
            user_id=qq_id,
            group_id=gruop_id,
            group_name=group_name,
            group_data=group_data
        )
        if fun['status'] == 'default':
            if type(fun['function']) == str:
                await wws_bot.finish()
        elif fun['status'] == 'info':
            await wws_bot.send(fun['message'])
        else:
            function = fun['function']
            result = await function(fun['parameter'])
            if result['status'] == 'ok':
                await wws_bot.send(MessageSegment.image(result['img']))
            elif result['status'] == 'info':
                await wws_bot.send(result['message'])
            else:
                await wws_bot.send(result['message'])
                if debug:
                    await bot.send_private_msg(user_id=superuser, message='发生错误：'+str(result['error']))
    except ActionFailed:
        return False
    except Exception:
        logger.error(traceback.format_exc())
        await bot.send(ev, "error")

import nonebot
from nonebot.adapters.onebot.v11.adapter import Adapter as OnebotV11Adapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(OnebotV11Adapter)

nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run()
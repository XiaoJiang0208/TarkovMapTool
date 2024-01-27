import requests  # 导入requests库用于发起HTTP请求。
import json  # 导入json库用于处理JSON数据。
import time  # 导入time库用于控制事件流（例如等待）。

# 定义房间号变量。
roomid = 'test'
# 定义玩家ID变量。
playerid = 'vp'
# 定义服务器地址变量，这里是Flask应用运行的本地地址。
server = 'http://127.0.0.1:5000/'

# 定义一个函数，用于发送玩家数据到服务器，并返回服务器的响应。
def setPlayerData(marker) -> dict:
    # 发送POST请求到服务器，包含玩家ID和标记信息。
    PlayerData = requests.post(server + roomid, json={'player': playerid, 'marker': marker}).json()
    return PlayerData  # 返回服务器响应的JSON数据。

# 主程序入口。
if __name__ == "__main__":
    i = 1600  # 初始化标记的left属性值。
    s = 20  # 初始化标记的变化速度和方向。
    # 开始无限循环。
    while True:
        time.sleep(2)  # 每次循环等待两秒钟。
        # 如果标记的left属性值超过3000，改变方向向左移动。
        if i > 3000:
            s = -20
        # 如果标记的left属性值低于1500，改变方向向右移动。
        if i < 1500:
            s = 20
        i += s  # 更新标记的left属性值。
        # 尝试发送更新后的玩家标记到服务器。
        try:
            # 打印服务器返回的更新后的玩家数据。
            print(setPlayerData(f"left: {i}px; top: 1300px; width: 10px; height: 10px;"))
        # 如果请求过程中发生异常，捕获异常并打印。
        except Exception as e:
            print(e)

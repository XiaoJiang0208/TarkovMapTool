import signal
import requests
import json
import time


#房间号
roomid='test1'
#用户id
playerid='vp'
#联机服务器
server='http://everyspower.xyz:5000/'

def setPlayerData(marker)->dict:
    PlayerData=requests.post(server+roomid,json={'player':playerid,'marker':marker}).json()
    print(PlayerData)
    return PlayerData

"""def offline():
    '''注册退出事件，退出时从服务器离线'''
    print(1)
    setPlayerData('')
signal.signal(signal.SIGINT, offline)  # 捕捉 Ctrl+C
signal.signal(signal.SIGTERM, offline)"""#无用😢

if __name__ == "__main__":
    i=1600
    s=20
    while True:
        time.sleep(2)
        if i > 3000:
            s=-20
        if i < 1500:
            s=20
        i+=s
        try:
            print(setPlayerData(f"left: {i}px; top: 1300px; width: 10px; height: 10px;"))
        except Exception as e:
            print(e)
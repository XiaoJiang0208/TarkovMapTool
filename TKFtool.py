# 导入所需的库
from selenium import webdriver 
from selenium.webdriver.common.by import By
import requests
import keyboard as kb
import time
import os
import pathlib
import json
import traceback

# 定义屏幕截图将被保存的路径
ImgPath = str(pathlib.Path.home()) + '\\Documents\\Escape from Tarkov\\Screenshots\\'
# 设置刷新玩家位置的时间间隔（以秒为单位）
sleeptime = 1.5
# 控制自动截图功能的标志
auto = False
# 启动自动截图的快捷键
on_auto = 'f5'
# 关闭自动截图的快捷键
off_auto = 'f6'
# 截图键
key = 'j'
# 房间号
roomid = ''
# 用户ID
playerid = ''
# 联机服务器地址
server = ''

# 用于存储上一个文件名的临时变量
tmp = ''
def getPosition():
    # 获取截图文件夹中的文件列表，移除最新的截图文件，并返回文件名
    global tmp
    dir = os.listdir(ImgPath)
    if len(dir) == 0:
        return tmp
    tmp = dir[0]
    os.remove(ImgPath + tmp)
    return tmp

def InitDir():
    # 初始化截图目录，移除所有现有截图
    dir = os.listdir(ImgPath)
    for d in dir:
        os.remove(ImgPath + d)

def getkb(event):
    # 键盘事件处理函数，控制自动截图的开关
    global auto
    if event.name == on_auto:
        auto = True
    if event.name == off_auto:
        auto = False

def getConfig():
    # 读取或创建配置文件，并更新设置
    global ImgPath, sleeptime, on_auto, off_auto, key, roomid, playerid, server
    if 'setting.json' not in os.listdir('.\\'):
        with open('setting.json', 'w') as setting:
            cfg = json.dumps({'ImgPath': ImgPath,
                              'sleeptime': sleeptime,
                              'on_auto': on_auto,
                              'off_auto': off_auto,
                              'key': key,
                              'roomid': roomid,
                              'playerid': playerid,
                              'server': server})
            setting.write(cfg)
    with open('setting.json', 'r') as setting:
        cfg = json.loads(setting.read())
        ImgPath = cfg['ImgPath']
        sleeptime = cfg['sleeptime']
        on_auto = cfg['on_auto']
        off_auto = cfg['off_auto']
        key = cfg['key']
        roomid = cfg['roomid']
        playerid = cfg['playerid']
        server = cfg['server']

def getMarker(driver: webdriver.Edge):
    # 从网页中获取标记的样式属性
    marker = driver.find_element(By.XPATH, "//*[@class='marker']")
    return marker.get_attribute('style').rstrip("visibility: hidden;") + ";"

def setMarker(driver: webdriver.Edge, id, ps='', color='#f9ff01'):
    # 在地图上设置一个新的标记
    if not id:
        id = 'offline'
    try:
        driver.find_element(By.XPATH, f"//*[@id='{id}']")
    except:
        # 如果标记不存在，则通过JavaScript创建一个新的标记
        js = f'''var map = document.querySelector("#map");
                 map.insertAdjacentHTML("beforeend", "<div id='{id}' class='marker' style='{ps}background:{color};'></div>");'''
        driver.execute_script(js)
        return
    if ps == '':
        # 如果位置信息为空，移除标记
        js = '''
        var marker = document.querySelector("#{id}");
        marker.remove();
        '''
    # 更新标记的样式
    js = f'''var marker = document.querySelector("#{id}");
             marker.setAttribute('style', '{ps}background:{color};');'''
    driver.execute_script(js)

def setPlayerData(marker) -> dict:
    # 打印日志，并将玩家数据发送到服务器
    print(1)
    print({'player': playerid, 'marker': marker})
    PlayerData = requests.post(server + roomid, json={'player': playerid, 'marker': marker}).json()
    print(2)
    return PlayerData

if __name__ == "__main__":
    # 主函数
    driver = webdriver.Edge()
    driver.get('https://tarkov-market.com/maps/ground-zero')
    InitDir()
    getConfig()
    kb.on_press(getkb)
    playerList = []
    while True:
        time.sleep(sleeptime)
        try:
            if auto:  # 如果启用自动截图，则触发截图键
                kb.press_and_release(key)
            # 在网页中填写截图文件名并提交
            bt = driver.find_element(By.XPATH, "//*[@placeholder='Paste file name here']")
            bt.click()
            time.sleep(0.01)
            bt.send_keys(getPosition())
            # 获取并隐藏当前标记，设置新的标记
            ps = getMarker(driver)
            marker = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div/div[4]/div")
            driver.execute_script('arguments[0].style.visibility="hidden";', marker)
            setMarker(driver, playerid, ps, color="#6aff00")
            # 处理多玩家数据
            if server and roomid and playerid:
                print("处理多人")
                datas = setPlayerData(getMarker(driver))
                for player in playerList:
                    setMarker(driver, player)
                for player in datas.keys():
                    if player != playerid:
                        setMarker(driver, player, datas[player])
                playerList = datas.keys()
                print(setPlayerData(getMarker(driver)))
        except:
            # 异常处理
            print(traceback.format_exc())
            try:
                driver.find_element(By.XPATH, "//button[contains(text(),'Where am i?')]").click()
                print('获取输入框。。。')
            except:
                print('无法打开输入框')

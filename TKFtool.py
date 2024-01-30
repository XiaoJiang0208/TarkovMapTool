from selenium import  webdriver
from selenium.webdriver.common.by import By
import requests
import keyboard as kb
import time
import os
import pathlib
import json
import traceback
import atexit


#截图路径
ImgPath=str(pathlib.Path.home())+'\\Documents\\Escape from Tarkov\\Screenshots\\'
#位置刷新间隔（秒）
sleeptime=1.5
#自动截图
auto=False
#启动自动截图
on_auto='f5'
#关闭自动截图
off_auto='f6'
#截图键
key='j'
#房间号
roomid=''
#用户id
playerid=''
#联机服务器
server=''


tmp=''
def getPosition():
    '''获取截图位置信息'''
    global tmp
    dir=os.listdir(ImgPath)
    if len(dir)==0:
        return tmp
    tmp=dir[0]
    os.remove(ImgPath+tmp)
    return tmp

def InitDir():
    '''初始化截图文件夹'''
    dir=os.listdir(ImgPath)
    for d in dir:
        os.remove(ImgPath+d)

def setScreenShoot(event):
    '''设置自动截图状态'''
    global auto
    if event.name==on_auto:
        auto=True
    if event.name==off_auto:
        auto=False

def getConfig():
    '''获取配置文件配置'''
    global ImgPath, sleeptime, on_auto, off_auto, key, roomid, playerid, server
    if 'setting.json' not in os.listdir('.\\'):
        with open('setting.json','w') as setting:
            cfg = json.dumps({'ImgPath':ImgPath,
                            'sleeptime':sleeptime,
                            'on_auto':on_auto,
                            'off_auto':off_auto,
                            'key':key,
                            'roomid':roomid,
                            'playerid':playerid,
                            'server':server})
            setting.write(cfg)
    with open('setting.json','r') as setting:
        cfg = json.loads(setting.read())
        ImgPath=cfg['ImgPath']
        sleeptime=cfg['sleeptime']
        on_auto=cfg['on_auto']
        off_auto=cfg['off_auto']
        key=cfg['key']
        roomid=cfg['roomid']
        playerid=cfg['playerid']
        server=cfg['server']

def getMarker(driver:webdriver.Edge):
    '''获取地图标记位置'''
    marker=driver.find_element(By.XPATH, "//*[@class='marker']")
    return marker.get_attribute('style').rstrip("visibility: hidden;")+";"

def setMarker(driver:webdriver.Edge,id,ps='',color='#f9ff01'):
    '''设置新marker位置'''
    if not id:
        id='offline'
    try:
        driver.find_element(By.XPATH, f"//*[@id='{id}']")
    except:
        js=f'''var map=document.querySelector("#map");
            map.insertAdjacentHTML("beforeend","<div id='{id}' class='marker' style='{ps}background:{color};'></div>");'''
        driver.execute_script(js)
        return
    if ps=='':
        js=f'''
        var marker=document.querySelector("#{id}");
        marker.remove();
        '''
    js=f'''var marker=document.querySelector("#{id}");
            marker.setAttribute('style','{ps}background:{color};');'''
    driver.execute_script(js)


def setPlayerData(marker)->dict:
    '''上传玩家数据到在线,返回所有玩家数据'''
    print({'player':playerid,'marker':marker})
    PlayerData=requests.post(server+roomid,json={'player':playerid,'marker':marker}).json()
    return PlayerData

"""@atexit.register
def offline():
    '''注册退出事件，退出时从服务器离线'''
    setPlayerData('')"""#无法使用

if __name__ == "__main__":
    getConfig()
    driver = webdriver.Edge()
    driver.get('https://tarkov-market.com/maps/ground-zero')
    InitDir()
    kb.on_press(setScreenShoot)#绑定键盘事件调整键盘事件
    playerList=[]
    while True:
        time.sleep(sleeptime)
        try:
            if auto: #是否自动截图
                kb.press_and_release(key)
            bt=driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div/div[1]/div/input")
            bt.click()
            time.sleep(0.01)
            bt.send_keys(getPosition())
            #新的标记渲染机制
            ps=getMarker(driver)
            marker=driver.find_element(By.XPATH,"/html/body/div/div/div/div[2]/div/div/div[4]/div")
            driver.execute_script('arguments[0].style.visibility="hidden";',marker)
            setMarker(driver,playerid,ps,color="#6aff00")
            #处理多人
            if server and roomid and playerid:
                print("处理多人")
                datas=setPlayerData(getMarker(driver))
                for player in playerList:
                    if player !=playerid:
                        setMarker(driver,player)
                for player in datas.keys():
                    if player != playerid:
                        setMarker(driver,player,datas[player])
                playerList=datas.keys()
                print(setPlayerData(getMarker(driver)))
        except:
            print(traceback.format_exc())
            try:
                driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div/div[1]/div/button").click()
                print('获取输入框。。。')
            except:
                print('无法打开输入框')
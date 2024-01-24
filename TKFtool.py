from selenium import  webdriver 
from selenium.webdriver.common.by import By
import requests
import keyboard as kb
import time
import os
import pathlib
import json
import traceback


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


tmp=''
def getPosition():
    global tmp
    dir=os.listdir(ImgPath)
    if len(dir)==0:
        return tmp
    tmp=dir[0]
    os.remove(ImgPath+tmp)
    return tmp

def InitDir():
    dir=os.listdir(ImgPath)
    for d in dir:
        os.remove(ImgPath+d)

def getkb(event):
    global auto
    if event.name==on_auto:
        auto=True
    if event.name==off_auto:
        auto=False

def getConfig():
    global ImgPath, sleeptime, on_auto, off_auto, key, roomid, playerid, server
    if 'setting.json' not in os.listdir('.\\'):
        with open('setting.json','w') as setting:
            cfg = json.dumps({'ImgPath':ImgPath,
                            'sleeptime':sleeptime,
                            'on_auto':on_auto,
                            'off_auto':off_auto,
                            'key':key})
            setting.write(cfg)
    with open('setting.json','r') as setting:
        cfg = json.loads(setting.read())
        ImgPath=cfg['ImgPath']
        sleeptime=cfg['sleeptime']
        on_auto=cfg['on_auto']
        off_auto=cfg['off_auto']
        key=cfg['key']
        
def getMarker(driver:webdriver.Edge):
    marker=driver.find_element(By.XPATH, "//*[@class='marker']")
    return marker.get_attribute('style').rstrip("visibility: hidden;")+";"

def setMarker(driver:webdriver.Edge,id,ps='',color='#f9ff01'):
    '''设置新marker'''
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
    print(1)
    print({'player':playerid,'marker':marker})
    PlayerData=requests.post(server+roomid,json={'player':playerid,'marker':marker}).json()
    print(2)
    return PlayerData

if __name__ == "__main__":
    getConfig()
    driver = webdriver.Edge()
    driver.get('https://tarkov-market.com/maps/ground-zero')
    InitDir()
    kb.on_press(getkb)
    playerList=[]
    while True:
        time.sleep(sleeptime)
        try:
            if auto: #是否自动截图
                kb.press_and_release(key)
            bt=driver.find_element(By.XPATH, "//*[@placeholder='Paste file name here']")
            bt.click()
            time.sleep(0.01)
            bt.send_keys(getPosition())
            #新的标记渲染机制
            ps=getMarker(driver)
            marker=driver.find_element(By.XPATH,"/html/body/div/div/div/div[2]/div/div/div[4]/div")
            driver.execute_script('arguments[0].style.visibility="hidden";',marker)
            setMarker(driver,'',ps,color="#6aff00")
        except:
            print(traceback.format_exc())
            try:
                driver.find_element(By.XPATH, "//button[contains(text(),'Where am i?')]").click()
                print('获取输入框。。。')
            except:
                print('无法打开输入框')
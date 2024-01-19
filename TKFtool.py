from selenium import  webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import keyboard as kb
import time
import os

#截图路径
ImgPath='C:/Users/18370/Documents/Escape from Tarkov/Screenshots/'
#位置刷新间隔（秒）
sleeptime=2.5
#自动截图
auto=False
#启动自动截图
on_auto='f5'
#关闭自动截图
off_auto='f6'
#截图键
key='j'

def getPosition():
    global tmp
    dir=os.listdir('C:/Users/18370/Documents/Escape from Tarkov/Screenshots/')
    if len(dir)==0:
        return tmp
    tmp=dir[0]
    os.remove(ImgPath+tmp)
    return tmp

def InitDir():
    dir=os.listdir('C:/Users/18370/Documents/Escape from Tarkov/Screenshots/')
    for d in dir:
        os.remove(ImgPath+d)

def getkb(event):
    global auto
    if event.name==on_auto:
        auto=True
    if event.name==off_auto:
        auto=False

driver = webdriver.Edge()
driver.get('https://tarkov-market.com/maps/ground-zero')
InitDir()
while True:
    time.sleep(sleeptime)
    kb.on_press(getkb)
    try:
        bt=driver.find_element(By.XPATH, "//*[@placeholder='Paste file name here']")
        if auto: #是否自动截图
            kb.press_and_release(key)
        bt.send_keys(getPosition())
        driver.find_element(By.XPATH, "//button[contains(text(),'Where am i?')]").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Where am i?')]").click()
    except:
        try:
            driver.find_element(By.XPATH, "//button[contains(text(),'Where am i?')]").click()
            print('获取输入框。。。')
        except:
            print('无法打开输入框')

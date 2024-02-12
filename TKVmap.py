#导昏死过去
import json
import pathlib
from typing import Any
import pygame as pg
from pygame.locals import *
import os
import traceback
from scipy.spatial.transform import Rotation as R
import ctypes
import toml
#性能测试库
#置顶
import win32gui
import win32con




class Mouse(pg.sprite.Sprite):
    '''鼠标'''
    def __init__(self) -> None:
        super().__init__()
        self.image=pg.Surface((1,1))
        self.image.fill((0,0,0,0))
        self.rect=self.image.get_rect()
        self.rect.center=pg.mouse.get_pos()

    def getMove(self) -> tuple:
        '''获取鼠标移动值'''
        return (pg.mouse.get_pos()[0]-self.rect.center[0],pg.mouse.get_pos()[1]-self.rect.center[1])

    def update(self, target:pg.Surface) -> None:
        self.image.get_rect().center=pg.mouse.get_pos()
        self.rect.center=pg.mouse.get_pos()
        target.blit(self.image,self.rect)
        return super().update()


class Map(pg.sprite.Sprite):
    '''互动地图'''
    def __init__(self,dir:str) -> None:
        super().__init__()
        self.dir=dir
        self.raw=pg.image.load(self.dir+"/1.png").convert_alpha()
        self.size=1.0
        self.image=pg.transform.scale_by(self.raw,self.size)
        self.rect=self.image.get_rect()

    def move(self,x,y) -> None:
        '''向xy轴正半轴移动'''
        self.rect.center=(self.rect.center[0]+x,self.rect.center[1]+y)

    def resize(self,p) -> None:
        '''缩放'''
        self.size+=p
        if self.size<0.09:
            self.size=0.09
        if self.size>1:
            self.size=1
        tmp=self.rect
        self.image=pg.transform.scale_by(self.raw,self.size)
        self.rect=self.image.get_rect()
        self.rect.center=tmp.center

    def changeLevel(self,level):
        '''控制地图层级'''
        self.raw=pg.image.load(self.dir+"/"+str(level)+".png").convert_alpha()
        rt=self.rect
        self.rect=self.image.get_rect()
        self.rect.center=rt.center
        self.image=pg.image.load(self.dir+"/"+str(level)+".png").convert_alpha()
        self.image=pg.transform.scale_by(self.raw,self.size)
        #self.move((oldwidth-self.showimage.get_width())7/2,(oldheight-self.showimage.get_height())/2)

    def update(self, target:pg.Surface) -> None:
        target.blit(self.image,self.rect)
        return super().update()


class Player(pg.sprite.Sprite):
    '''玩家标记'''
    #-0.04
    def __init__(self,dir:str) -> None:
        self.ruler=toml.load(dir+"/setting.toml")["player"]["ruler"]
        self.raw=pg.image.load("./marks/player.png").convert_alpha()
        self.image=pg.transform.scale_by(self.raw,0.2)
        self.rect=self.image.get_rect()
        self.size=toml.load(dir+"/setting.toml")["player"]["size"]
        self.reangle=toml.load(dir+"/setting.toml")["player"]["reangle"]
        self.angle=0
        super().__init__()
    def update(self, target:pg.Surface, map:Map) -> None:
        resize=map.size*self.ruler#fuk
        ps=getPosition()
        #如果大小发生变化改变大小
        if self.size!=map.size:
            self.size=map.size
            self.image=pg.transform.rotozoom(self.raw,-(self.angle+self.reangle),self.size)
            self.rect=self.image.get_rect()
        #角度变化
        if self.angle!=ps[1]:
            self.angle=ps[1]
            self.image=pg.transform.rotozoom(self.raw,-(self.angle+self.reangle),self.size)
            self.rect=self.image.get_rect()
        self.rect.center=(map.rect.centerx-ps[0][2]*resize,map.rect.centery-ps[0][0]*resize)
        target.blit(self.image,self.rect)
        return super().update()

class Button(pg.sprite.Sprite):
    '''按钮控件'''
    def __init__(self,text:str="Button",border:int=5) -> None:
        super().__init__()
        self.font=pg.font.Font("./fonts/MSYH.TTC")
        self.text=self.font.render(text,(27, 30, 46),(243, 243, 245))
        self.image=pg.Surface((self.text.get_size()[0]+border,self.text.get_size()[1]+border))
        self.rect=self.image.get_rect()

    def setText(self,text) -> None:
        '''设置文本'''
        self.text=self.font.render(text,(27, 30, 46),(243, 243, 245))
        self.rect=self.image.get_rect()

    def setBorder(self,bd) -> None:
        '''设置边框'''
        self.image=pg.Surface((self.text.get_size()[0]+bd,self.text.get_size()[1]+bd))

    def setPosition(self,ps:list) -> None:
        '''设置位置'''
        self.rect.centerx=ps[0]+self.image.get_width()/2
        self.rect.centery=ps[1]+self.image.get_height()/2

    def update(self, target:pg.Surface) -> None:
        target.blit(self.image,self.rect)
        target.blit(self.text,self.rect)


def InitDir():
    '''初始化截图文件夹'''
    dir=os.listdir(ImgPath)
    for d in dir:
        os.remove(ImgPath+d)

def quaternion2euler(quaternion):
    '''计算旋转角'''
    r = R.from_quat(quaternion)
    euler = r.as_euler('xyz', degrees=True)
    return euler

tmp=[(0,0,0),0.0]
def getPosition() -> list:
    '''获取截图位置信息'''
    global tmp
    dir=os.listdir(ImgPath)
    if len(dir)==0:
        return tmp
    #求旋转角
    angle=dir[0].split("_")[2].split(",")
    angle[3]=angle[3][:-7]
    angle=list(map(float,angle))
    angle=quaternion2euler(angle)
    if abs(angle[0])<90:
        angle=angle[1] if angle[1]>0 else angle[1]+360
    elif abs(angle[0])>=90:
        angle=180-angle[1] if angle[1]>0 else 180-angle[1]
    print(angle)
    tmp=[list(map(float,dir[0].split("_")[1].split(","))),angle]
    os.remove(ImgPath+dir[0])
    return tmp


#截图储存位置
ImgPath=''


def createmap(dir:str,imgpath):
    #各种初始化:/
    global ImgPath
    ImgPath=imgpath
    InitDir()
    pg.init()
    clock=pg.time.Clock()
    MainWindow=pg.display.set_mode((800,600),pg.RESIZABLE)
    pg.display.set_caption(dir.split("/")[1])
    #i=ctypes.windll.user32.GetLastError()
    win32gui.SetWindowPos(pg.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    #初始化地图
    factory=Map(dir)
    factory.rect.center=[pg.display.get_surface().get_size()[0]/2,pg.display.get_surface().get_size()[1]/2]
    factory.resize(-0.8)
    #初始化鼠标
    mouse=Mouse()
    #初始化玩家
    player=Player(dir)
    #初始化控件
    testup=Button("up")
    testup.setBorder(15)
    testup.setPosition((0,0))
    testdown=Button("down")
    testdown.setBorder(15)
    testdown.setPosition((0,20))
    level=1

    running=True
    while running:
        clock.tick(60)
        #事件处理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False
            if event.type == pg.MOUSEMOTION:
                #地图拖拽
                if pg.mouse.get_pressed()[0]:
                    factory.move(mouse.getMove()[0],mouse.getMove()[1])
            if event.type == pg.MOUSEBUTTONDOWN:
                #翻到上层
                if pg.sprite.collide_mask(mouse,testup):
                    level+=1
                    if level>3:
                        level=0
                    factory.changeLevel(level)
                #翻到下层
                if pg.sprite.collide_mask(mouse,testdown):
                    level-=1
                    if level<0:
                        level=3
                    factory.changeLevel(level)
                #地图缩放
                if event.button == 4:
                    factory.resize(0.05)
                if event.button == 5:
                    factory.resize(-0.05)


        #界面绘制
        MainWindow.fill((36, 40, 59))

        #渲染互动地图
        factory.update(MainWindow)

        #渲染玩家
        player.update(MainWindow,factory)

        #渲染控件
        testup.update(MainWindow)
        testdown.update(MainWindow)

        #渲染鼠标
        mouse.update(MainWindow)
        '''it.setPosition([x,0])
        it.shader(MainWindow)'''
        pg.display.update()
    pg.quit()

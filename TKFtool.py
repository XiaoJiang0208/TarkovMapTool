#导昏死过去
import json
import pathlib
from typing import Any
import pygame as pg
from pygame.locals import *
import os
import traceback
#性能测试库
from pyinstrument import Profiler
profiler = Profiler()


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
        self.size+=p
        if self.size<0.09:
            self.size=0.09
        if self.size>1:
            self.size=1
        oldwidth=self.image.get_width()
        oldheight=self.image.get_height()
        self.image=pg.transform.scale_by(self.raw,self.size)
        self.rect=self.image.get_rect()
        #self.move((oldwidth-self.image.get_width())/2,(oldheight-self.image.get_height())/2)

    def changeLevel(self,level):
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
    def __init__(self) -> None:
        self.image=pg.image.load("./marks/player.png").convert_alpha()
        self.rect=self.image.get_rect()
        super().__init__()
    def update(self, target:pg.Surface, map:Map) -> None:
        resize=map.size*22.7#fuk
        ps=getPosition()
        self.rect.center=(map.rect.centerx-ps[0][2]*resize,map.rect.centery-ps[0][0]*resize)
        target.blit(self.image,self.rect)
        return super().update()

class Button(pg.sprite.Sprite):
    '''按钮控件'''
    def __init__(self,text:str) -> None:
        super().__init__()
        ft=pg.font.Font("./maps/ARIAL.TTF")
        self.text=ft.render(text,(27, 30, 46),(243, 243, 245))
        self.image=pg.Surface(self.text.get_size())
        self.rect=self.image.get_rect()
        self.border=0

    def setBorder(self,bd):
        self.border=bd
        self.image=pg.Surface((self.text.get_width()+self.border,self.text.get_height()+self.border))

    def update(self, target:pg.Surface) -> None:
        target.blit(self.image,self.rect)
        target.blit(self.text,self.rect)


def InitDir():
    '''初始化截图文件夹'''
    dir=os.listdir(ImgPath)
    for d in dir:
        os.remove(ImgPath+d)

tmp=[(0,0,0),1]
def getPosition() -> list:
    '''获取截图位置信息'''
    global tmp
    dir=os.listdir(ImgPath)
    if len(dir)==0:
        return tmp
    tmp=[list(map(float,dir[0].split("_")[1].split(","))),float(dir[0].split("_")[1].split(",")[1])]
    os.remove(ImgPath+dir[0])
    return tmp

def getConfig():
    '''获取配置文件配置'''
    global ImgPath, sleeptime, on_auto, off_auto, key, roomid, playerid, server
    if 'setting.json' not in os.listdir('.\\'):
        with open('setting.json','w') as setting:
            cfg = json.dumps({'ImgPath':ImgPath})
            setting.write(cfg)
    with open('setting.json','r') as setting:
        cfg = json.loads(setting.read())
        ImgPath=cfg['ImgPath']


ImgPath=str(pathlib.Path.home())+'\\Documents\\Escape from Tarkov\\Screenshots\\'


if __name__ == '__main__':
    InitDir()
    getConfig()
    pg.init()
    clock=pg.time.Clock()
    MainWindow=pg.display.set_mode((800,600),pg.RESIZABLE)
    pg.display.set_caption("test")
    x=1.0

    #初始化地图
    factory=Map("./maps/factory")
    factory.rect.center=[pg.display.get_surface().get_size()[0]/2,pg.display.get_surface().get_size()[1]/2]
    factory.resize(-0.8)
    #初始化鼠标
    mouse=Mouse()
    #初始化玩家
    player=Player()
    #初始化控件
    testup=Button("up")
    testup.setBorder(5)
    testdown=Button("down")
    testdown.setBorder(5)
    testdown.rect.top=20
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
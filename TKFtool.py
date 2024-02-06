#导昏死过去
from typing import Any
import pygame as pg
from pygame.locals import *
import sys
import traceback


class ItemsBox():
    '''组件盒子'''
    def __init__(self,rootitem:pg.Surface,ps:list) -> None:
        self.RootItem=rootitem
        self.Items=dict()
        self.Position=ps

    def setPosition(self,ps:list) -> None:
        '''设置组件盒子位置'''
        self.Position=ps
    def getPosition(self) -> list:
        '''获取组件盒子位置'''
        return self.Position

    def addItem(self,name,item:pg.Surface,ps:list) -> None:
        '''添加组件
        name: 组件名称
        item: 组件实例
        ps: 相对位置
        '''
        self.Items[name]=[item,ps]

    def getItemPosition(self,itemname) -> list|None:
        '''获取组件绝对坐标
        Args:
            itemname: 组件名称
        return: 组件绝对坐标
        '''
        try:
            ps=[self.Position[0]+self.Items[itemname][1][0],self.Position[1]+self.Items[itemname][1][1]]
            return ps
        except Exception as e:
            print(e.args)
            print("====")
            print(traceback.format_exc())
            return None

    def shader(self,target:pg.Surface) -> None:
        '''渲染组件
        target: 目标组件
        ps: 组件盒子坐标
        '''

        target.blit(self.RootItem,self.Position)
        for key in self.Items.keys():
            target.blit(self.Items[key][0],self.getItemPosition(key))


class Mouse(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image=pg.Surface((2,2))
        self.image.fill('red')
        self.rect=self.image.get_rect()
        self.rect.center=pg.mouse.get_pos()
        self.oldPosition=self.rect.center

    def getMove(self) -> tuple:
        '''获取鼠标移动值'''
        #TODO: 这有问题md
        now=pg.mouse.get_pos()
        return (now[0]-self.oldPosition[0],now[1]-self.oldPosition[1])

    def update(self, target:pg.Surface) -> None:
        self.image.get_rect().center=pg.mouse.get_pos()
        self.rect.center=pg.mouse.get_pos()
        target.blit(self.image,self.rect)
        return super().update()


class Map(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image=pg.image.load("./maps/maps/Factory.webp")
        self.rect=self.image.get_rect()
        self.MoveToMouse=False
    def move(self,x,y):
        '''向xy轴正半轴移动'''
        self.rect.center=(self.rect.center[0]+x,self.rect.center[1]+y)
    def update(self, target:pg.Surface) -> None:
        target.blit(self.image,self.rect)
        return super().update()


if __name__ == '__main__':
    pg.init()
    clock=pg.time.Clock()
    MainWindow=pg.display.set_mode((800,600),pg.RESIZABLE)
    pg.display.set_caption("test")
    x=1.0

    maps=Map()
    mouse=Mouse()

    running=True
    while running:
        clock.tick(60)
        #事件处理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False
        #开始拖拽地图
        if pg.sprite.collide_mask(mouse,maps) and pg.mouse.get_pressed()[0]:
            print(mouse.getMove())
            mv=mouse.getMove()
            maps.move(mv[0],mv[1])

        #界面绘制
        MainWindow.fill((36, 40, 59))

        #处理互动地图
        maps.update(MainWindow)
        #处理鼠标
        mouse.update(MainWindow)
        '''it.setPosition([x,0])
        it.shader(MainWindow)'''
        pg.display.update()
pg.quit()
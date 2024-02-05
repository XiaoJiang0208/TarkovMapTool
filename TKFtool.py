#导昏死过去
import pygame
from pygame.locals import *
import sys
import traceback


class ItemsBox():
    '''组件盒子'''
    def __init__(self,rootitem:pygame.Surface,ps:list) -> None:
        self.RootItem=rootitem
        self.Items=dict()
        self.Position=ps

    def addItem(self,name,item:pygame.Surface,ps:list) -> None:
        '''添加组件
        name: 组件名称
        item: 组件实例
        ps: 相对位置
        '''
        self.Items[name]=[item,ps]

    def getItemPosition(self,itemname) -> list|None:
        '''获取组件绝对坐标
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

    def shader(self,target:pygame.Surface,ps:list) -> None:
        '''渲染组件
        target: 目标组件
        ps: 组件盒子坐标
        '''
        self.Position=ps
        target.blit(self.RootItem,ps)
        for item in self.Items.keys
            target.blit(item[0],)


if __name__ == '__main__':
    pygame.init()
    clock=pygame.time.Clock()
    MainWindow=pygame.display.set_mode((800,600))
    pygame.display.set_caption("test")
    img= pygame.image.load('./test.png')

    x=0
    while True:
        #事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        #界面绘制
        MainWindow.fill((36, 40, 59))
        MainWindow.blit(img,(x,0))
        pygame.display.update()
        clock.tick(60)
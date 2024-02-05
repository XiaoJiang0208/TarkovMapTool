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

    def setPosition(self,ps:list) -> None:
        self.Position=ps
    def getPosition(self) -> list:
        return self.Position

    def addItem(self,name,item:pygame.Surface,ps:list) -> None:
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

    def shader(self,target:pygame.Surface) -> None:
        '''渲染组件
        target: 目标组件
        ps: 组件盒子坐标
        '''

        target.blit(self.RootItem,self.Position)
        for key in self.Items.keys():
            target.blit(self.Items[key][0],self.getItemPosition(key))


if __name__ == '__main__':
    pygame.init()
    clock=pygame.time.Clock()
    MainWindow=pygame.display.set_mode((800,600))
    pygame.display.set_caption("test")
    img= pygame.image.load('./test.png')
    it=ItemsBox(img,[10,10])
    it.addItem("test",img,(10,10))
    x=0

    running=True
    while running:
        clock.tick(60)
        #事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
        #界面绘制
        MainWindow.fill((36, 40, 59))
        MainWindow.blit(img,(x,0))
        it.setPosition([x,0])
        it.shader(MainWindow)
        x+=1
        pygame.display.update()
pygame.quit()
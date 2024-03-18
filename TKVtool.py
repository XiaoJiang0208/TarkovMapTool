import os
import pathlib
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from TKVmap import createmap
import toml
import traceback


def setSetting(pg,key,value):
    '''设置设置'''
    try:
        open('./setting.toml', "a")
    except:
        traceback.print_exc(file=open('error.log','w+'))
        return None
    st=toml.load('./setting.toml')
    print(st)
    st[pg]=st.get(pg,dict())#没有选项就初始化
    st[pg][key]=value
    with open('./setting.toml','w') as f:
        toml.dump(st,f)

def getSetting(pg,key):
    '''获取设置'''
    try:
        st=toml.load('./setting.toml')
        return st[pg][key]
    except:
        traceback.print_exc(file=open('error.log','w+'))
        return None


def initSetting():
    #地图部分
    setSetting('map','screenshots',str(pathlib.Path.home())+'\\Documents\\Escape from Tarkov\\Screenshots\\')
    setSetting('map','autoshot','f5')
    setSetting('map','shot','j')


if __name__ == "__main__":
    if 'setting.toml' not in os.listdir('./'):
        print(1)
        initSetting()
    root=ttk.Window()
    root.geometry('800x600')
    root.title('TarkovMapTool')

    #书签也页
    notebook=ttk.Notebook(root)
    #notebook.grid(sticky=N+W+W+E)
    notebook.pack(side='top',fill='both',expand=YES)


    #地图页面
    pageMap=ttk.Frame(notebook)
    ttk.Button(pageMap,text="工厂",command=lambda : createmap('./maps/factory',getSetting('map','screenshots'))).grid(row=0,column=0)
    ttk.Button(pageMap,text="海关",command=lambda : createmap('./maps/customs',getSetting('map','screenshots'))).grid(row=0,column=1)


    #设置界面
    def st():
        #TODO: 设置逻辑
        pass
    def reset():
        #TODO: 重置逻辑
        pass
    pageSetting=ttk.Frame(notebook)
    ttk.Label(pageSetting,text="地图设置",font=('MSYH',14)).grid(row=0,column=0)
    #截图路径
    ttk.Label(pageSetting,text="截图路径:").grid(row=1,column=0)
    screenshots=ttk.Entry(pageSetting)
    screenshots.insert(0,getSetting('map','screenshots'))
    screenshots.grid(row=1,column=1)
    #保存
    ttk.Button(pageSetting,text='保存',command=st).grid(row=2,column=0)
    ttk.Button(pageSetting,text='重置',command=reset).grid(row=2,column=1)


    #添加书签页
    notebook.add(pageMap,text="地图")
    notebook.add(pageSetting,text="设置")


    root.mainloop()
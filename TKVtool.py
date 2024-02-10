import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from TKVmap import createmap
import toml
import traceback


def setSetting(pg,key,value):
    try:
        file=open('./setting.toml', "w")
    except:
        traceback.print_exc(file=open('error.log','w+'))
        return None
    st=toml.load('./setting.toml')
    st[pg]=st.get(pg,dict())#没有选项就初始化
    st[pg][key]=value
    toml.dump(st,file)

def getSetting(pg,key):
    try:
        st=toml.loads('./setting.toml')
        return st[pg][key]
    except:
        traceback.print_exc(file=open('error.log','w+'))
        return None


def initSetting():
    pass


if __name__ == "__main__":
    setSetting("gg","ff",1323)
    root=ttk.Window()
    root.geometry('800x600')
    root.title('TarkovMapTool')

    #书签也页
    notebook=ttk.Notebook(root)
    #notebook.grid(sticky=N+W+W+E)
    notebook.pack(side='top',fill='both',expand=YES)


    #地图页面
    pageMap=ttk.Frame(notebook)
    btFactory=ttk.Button(pageMap,text="工厂",command=lambda : createmap('./maps/factory'))
    btFactory.grid(row=0,column=0)
    ttk.Button(pageMap,text="tt").grid(row=1,column=1)
    #设置界面


    #添加书签页
    notebook.add(pageMap,text="地图")


    root.mainloop()
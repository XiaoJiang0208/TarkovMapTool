# 塔可夫实时地图工具

## 视频教程


## 安装和使用
1. 下载后运行
2. 打开自动生成的setting.json文件按照需求修改
    ```
    {"ImgPath": "自己的截图位置（不能有中文路径）",
    "sleeptime": 1.5,
    "on_auto": "自动截图键-默认f5",
    "off_auto": "关闭自动截图键-默认f6",
    "key": "游戏内截图键-默认j",
    "roomid": "多人房号",
    "playerid": "多人名称",
    "server": "多人服务器"}
    ```
3. 修改游戏内的截图键与上面设置的一致
4. 启动工具，并使用powerTory的剪切与锁定工具将地图置顶

## 多人联机
1.打开setting.json文件
- 和要联机的人输入同样的`roomid`值
- 修改自己的多人名称 `playerid`值
- 修改多人服务器`server`值，作者自建的服务器`http://everyspower.xyz:5000/`
    e.g. `"server":"http://everyspower.xyz:5000/"`

## 自建服务器
安装python运行库，编辑`TKFtoolServer.py`的最后一行`app.run("外网ip-默认127.0.0.1",端口-默认6000)`
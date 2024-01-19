# 塔可夫实时地图工具

## 视频教程
    

## 安装和使用
1. 安装python, 官网：`https://www.python.org/downloads/`
2. 安装依赖
    ```
    pip install selenium -i https://mirrors.aliyun.com/pypi/simple/
    pip install keyboard -i https://mirrors.aliyun.com/pypi/simple/
    ```
3. 改键位和设置
    打开源文件`TKFtool.py`按需求更改
    ```
    #截图路径
    ImgPath='C:/Users/18370/Documents/Escape from Tarkov/Screenshots/'
    #位置刷新间隔（秒）
    sleeptime=2
    #自动截图
    auto=False
    #启动自动截图
    on_auto='f5'
    #关闭自动截图
    off_auto='f6'
    #截图键
    key='j'
    ```
3.使用powerTory的剪切与锁定工具将地图置顶
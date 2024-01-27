# 导入Flask模块中的所有公共成员。
from flask import *

# 初始化Flask应用程序。
app = Flask(__name__)

# 初始化一个空的字典，用作简单的数据库来存储数据。
database = dict()

# 定义一个路由，可以捕获任何在根URL后的'page'参数，并且只响应POST请求。
@app.route('/<page>', methods=['POST'])
def index(page):
    # 获取JSON格式的请求数据，这里假设发送到此端点的请求内容是JSON格式。
    player = request.get_json()
    print(player)  # 在服务器控制台打印接收到的玩家数据。
    
    # 如果请求的'page'不在数据库字典的键中，则在数据库中为这个'page'创建一个新的字典。
    if page not in database.keys():
        print(1)  # 控制台输出1，作为日志信息，表明创建了一个新的页面记录。
        database[page] =    
    # 在特定'page'的字典中，以玩家名为键，标记(marker)为值，存储玩家数据。
    database[page][player['player']] = player['marker']
    
    # 将更新后的'page'字典转换为JSON格式并返回。
    return json.dumps(database[page])

# 运行Flask应用程序，默认监听127.0.0.1:5000。
app.run()

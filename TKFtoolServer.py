from flask import *
import datetime

app = Flask(__name__)

database=dict()
death=1

@app.route('/<page>', methods=['POST'])
def index(page):
    player=request.get_json()
    if page not in database.keys():
        database[page]={}
    database[page][player['player']]=player['marker']
    #重置死亡事件
    database[page]["borntime"]=int(datetime.datetime.now().strftime("%H"))
    #垃圾清理
    for page in database.keys():
        if database[page]["borntime"]<int(datetime.datetime.now().strftime("%H"))-death:
            database.pop(page)
    #输出数据
    for page in database.keys():
        print(f"roomid:{page}-{database[page]['borntime']}")
    return json.dumps(database[page])


app.run()
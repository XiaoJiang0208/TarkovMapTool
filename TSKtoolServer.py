from flask import *

app = Flask(__name__)

database=dict()

@app.route('/<page>', methods=['POST'])
def index(page):
    player=request.get_json()
    print(player)
    if database.get(page,True):
        print('ssssssss')
        database[page]={}
    database[page][player['player']]=player['marker']
    print(database)
    return json.dumps(database[page])

app.run()
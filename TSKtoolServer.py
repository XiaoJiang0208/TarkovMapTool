from flask import *

app = Flask(__name__)

database=dict()

@app.route('/<page>', methods=['POST'])
def index(page):
    player=request.get_json()
    print(player)
    if page not in database.keys():
        print(1)
        database[page]={}
    database[page][player['player']]=player['marker']
    print(database)
    return json.dumps(database[page])

app.run()
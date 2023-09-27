from sanic import Sanic
from sanic.response import json
from sanic.response import text
from sanic_cors import CORS
import psycopg2


app = Sanic(__name__)
CORS(app)


@app.route("/data")
async def get_data(request):
    with open("data.json", "r") as f:
        data = f.read()
        # print(data)
    return json({'code': 20000,
                 'data': data})


@app.route("/")
async def hello_world(request):
    return text("Hello, world.")


@app.route("/get-data")
async def get_record(request):
    print("get-data")
    conn = psycopg2.connect(
        host="192.168.197.59",
        database="postgres",
        user="postgres",
        password="12345678"
    )
    cur = conn.cursor()
    print("get-data_2")
    cur.execute("SELECT temperature FROM record")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()
    return json({'code': 20000,
                'data': rows})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5393, debug=False)

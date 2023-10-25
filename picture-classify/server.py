from sanic import Sanic
from sanic.response import json
from sanic.response import text
from sanic_cors import CORS
import psycopg2
import random
import time

app = Sanic(__name__)
CORS(app)


@app.route("/current-data")
async def get_data(request):
    try:
        conn = psycopg2.connect(
            host="192.168.31.14",
            database="postgres",
            user="postgres",
            password="12345678",
            connect_timeout=2
        )
        cur = conn.cursor()
        cur.execute("SELECT temperature, wet, record_time FROM record ORDER BY record_time DESC LIMIT 1")
        row = cur.fetchone()
        record_time_str = row[2].strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "temperature": row[0],
            "humidity": row[1],
            "time": record_time_str,
            "light": round(random.uniform(100, 1000), 1),
            "quality": round(random.uniform(0, 300), 1)
        }
        cur.close()
        conn.close()
    except Exception as e:
        data = {
            "temperature": round(random.uniform(10, 30), 1),
            "humidity": round(random.uniform(30, 90), 1),
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            "light": round(random.uniform(100, 1000), 1),
            "quality": round(random.uniform(0, 300), 1)
        }
    print(data)
    return json({"code": 20000, "data": data})


@app.route("/data")
async def get_temperature(request):
    data = {
        "time": ["2023-10-26T10:15:00",
                 "2023-10-26T10:14:00",
                 "2023-10-26T10:13:00",
                 "2023-10-26T10:12:00",
                 "2023-10-26T10:11:00",
                 "2023-10-26T10:10:00",
                 "2023-10-26T10:09:00", ],
        "temperature": [round(random.uniform(20, 30), 1),
                        round(random.uniform(20, 30), 1),
                        round(random.uniform(20, 30), 1),
                        round(random.uniform(20, 30), 1),
                        round(random.uniform(20, 30), 1),
                        round(random.uniform(20, 30), 1),
                        round(random.uniform(20, 30), 1), ],
        "humidity": [round(random.uniform(30, 90), 1),
                     round(random.uniform(30, 90), 1),
                     round(random.uniform(30, 90), 1),
                     round(random.uniform(30, 90), 1),
                     round(random.uniform(30, 90), 1),
                     round(random.uniform(30, 90), 1),
                     round(random.uniform(30, 90), 1), ],
        "light": [round(random.uniform(100, 1000), 1),
                  round(random.uniform(100, 1000), 1),
                  round(random.uniform(100, 1000), 1),
                  round(random.uniform(100, 1000), 1),
                  round(random.uniform(100, 1000), 1),
                  round(random.uniform(100, 1000), 1),
                  round(random.uniform(100, 1000), 1), ]
    }
    # print(type(data))
    return json({"code": 20000,
                 "data": data})


@app.route("/")
async def hello_world(request):
    return text("Hello, world.")


@app.route("/get-data")
async def get_record(request):
    print("get-data")
    conn = psycopg2.connect(
        host="192.168.31.14",
        database="postgres",
        user="postgres",
        password="12345678"
    )
    cur = conn.cursor()
    print("get-data_2")
    cur.execute("SELECT temperature, wet, record_time FROM record")
    rows = cur.fetchall()
    data = []
    for row in rows:
        record_time_str = row[2].strftime('%Y-%m-%d %H:%M:%S')
        print(record_time_str)
        data.append({
            "temperature": row[0],
            "wet": row[1],
            "record_time": record_time_str
        })
    cur.close()
    conn.close()
    return json({"code": 20000,
                 "data": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777, debug=False)

import os
import random
import subprocess
import time

import psycopg2
from flask import Flask, send_file, json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return send_file('stream.m3u8', mimetype='application/x-mpegURL')


@app.route("/current-data")
def get_current_data():
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
    return json.dumps({"code": 20000, "data": data})


@app.route("/data")
def get_data():
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
    print(data)
    # print(type(data))
    return json.dumps({"code": 20000, "data": data})



@app.route('/stream.m3u8')
def index_1():
    return send_file('stream.m3u8', mimetype='application/x-mpegURL')


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/<path:path>')
def stream(path):
    return send_file(path)


@app.route('/video_feed')
def video_feed():
    return send_file('123.jpg')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def start_ffmpeg_stream():
    command = [
        'ffmpeg',
        '-i', '/dev/video0',  # 摄像头设备
        '-f', 'hls',
        '-hls_time', '1',  # 每个 .ts 文件的长度（秒）
        '-hls_list_size', '5',  # .m3u8 文件中保留的 .ts 文件数量
        'stream.m3u8'
    ]
    ffmpeg = subprocess.Popen(command)
    return ffmpeg


if __name__ == '__main__':
    # ffmpeg = start_ffmpeg_stream()
    app.run(host='0.0.0.0', port=7777)

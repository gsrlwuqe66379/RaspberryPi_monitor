from flask import *
import cv2
import logging as rel_log
from datetime import timedelta
from flask_cors import CORS
from detect import VideoCamera

app = Flask(__name__)
cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})  # 解决跨域问题,vue请求数据时能用上


@app.route('/')
def index():
    return render_template('index2.html')  # template文件夹下的index.html


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

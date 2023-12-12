# Raspberrypi monitor project

泥电连续性综合设计


## Show Raspberrypi Sensor data
采集与展示树莓派传感器数据

### 采集数据并上传数据库
这里使用postgreSQL数据库  
传感器采集原始模拟数据数字化处理后每分钟上传一次  
失败则5s后重试  

```python
import psycopg2
import RPi.GPIO as GPIO
from pin_dic import pin_dic
import time

######################
# 省略数据采集与处理代码 #
######################

conn = psycopg2.connect(
                        database="postgres",
                        user="postgres",
                        password="11111111",
                        host="192.168.1.106",
                        port="5432")  
# 根据不同数据库和网络自行修改连接配置     
cursor = conn.cursor()
# 创建游标连接数据库

try: 
    while True:
        flag, result = m_DHT11.read_DHT()        
        # 此处只上传温度湿度数据
        # 可以根据需要上传其他数据如烟雾浓度光照等
        if flag:
            #print(datetime.datetime.today())
            print("温度: %-3.1f C  湿度: %-3.1f %% " %(result[0],result[1]))
            insert_batch(result)
            time.sleep(60)
        else:                
            print("ERROR")                
            time.sleep(5)    
except KeyboardInterrupt:
    print('\n Ctrl + C QUIT')
    # 关闭游标
    cursor.close()
    # 关闭数据库连接
    conn.close()
finally:
    GPIO.cleanup()
# 连接数据库并上传采集的温度湿度数据
# 失败则5s后重试
# 数据库中创建表
# 接受上传数据   
```

### 从数据库获取数据并展示在前端页面
使用python sanic框架来连接数据库获取存储的数据  
（其他异步类flask框架均可实现）
并响应前端请求返回json格式数据  


```python

from sanic import Sanic
from sanic.response import json
from sanic.response import text
import psycopg2

# 创建后端服务连接数据库并返回json格式数据
app = Sanic(__name__)

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
    # 连接数据库
    # print("get-data_2")
    cur.execute("SELECT temperature, wet, record_time FROM record")
    rows = cur.fetchall()
    # 获取查询结果
    # 此处对全表进行查询返回，可以根据需要修改查询为最近一次或者多次而非全表
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
    # 格式化数据为json
    # 关闭数据库连接
    return json({"code": 20000,
                 "data": data})
    # 此处20000 为前端自定状态码，可根据需要修改

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777, debug=False)
    # 运行服务
```

### 前端展示

在以上基础上
直接访问127:0.0.17777即可查看记录的温湿度数据  

![访问效果图](/uesless/1.png)
  
此时只展示了所有原始数据，需要对数据进行可视化处理  
并减少数据查询量因此需要设计多种接口  
比如后面会使用的getcurrentdata即为返回最近一次数据的接口  
前端展示使用vue框架和百度的ECharts可视化图表  

vue-frontend/src/views/dashboard/admin/components/PanelGroup.vue
```html
<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('newVisitis')">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Sensor's Time
          </div>
          <p class="card-panel-num">{{ time }}</p>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('temperature')">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="theme" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Temperature
          </div>
          <count-to :start-val=oldtemperature :end-val=temperature :duration="3000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('humidity')">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="example" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Humidity
          </div>
          <count-to :start-val=oldhumidity :end-val=humidity :duration="3200" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('light')">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="eye" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Light Intensity
          </div>
          <count-to :start-val=oldlight :end-val=light :duration="3600" class="card-panel-num" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>
```

```js
// 部分核心数据接收代码 
import { getcurrentSensorData } from '@/api/sensor'
// 为代码规范将数据查询api与前端展示分离
methods: {
    fetchData() {
      this.oldtemperature = this.temperature
      this.oldhumidity = this.humidity
      this.oldlight = this.light
      getcurrentSensorData().then(response => {
        // console.log(response.data)
        const data = response.data
        console.log(data)
        const time = data['data'][0].time.substring(11, 19)
        const temperature = data['data'][0].temperature
        const humidity = data['data'][0].humidity
        const light = data['data'][0].light
        this.time = time
        this.temperature = temperature
        this.humidity = humidity
        this.light = light
        // 请求数据并进行数据处理
      }).catch(err => {
        console.log(err)
      })
    }},
  created() {
      this.fetchData()
      }
// vue-frontend/src/api/sensor.js

import request from '@/utils/request'

export function getcurrentSensorData() {
  return request({
    url: 'http://localhost:7777/current-data',
    method: 'get',
  })
}
// 通过访问后端api获取数据
```

![前端展示效果图](/uesless/2.png)

## Raspberrypi + picamera
树莓派摄像头与流式传输画面

### Installation

```bash
$ sudo apt-get install python-flask
$ sudo pip install picamera
```

### Run it

```bash
$ cd raspberry-camera/
$ python appCam.py
```

![](image.png)

## Frontend 


### Installation
```bash
$ cd vue-frontend
$ npm install
```
###
```bash
$ npm run dev
```

### Todo
- [X] 后端flask框架
- [X] 图像识别接口      
- [ ] 后台图片上传返回识别结果  
- [ ] 前端展示识别结果   
- [ ] 前端控制支持      


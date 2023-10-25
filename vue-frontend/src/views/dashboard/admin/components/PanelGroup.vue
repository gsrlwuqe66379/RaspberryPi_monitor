<template>
  <el-row :gutter="40" class="panel-group">
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
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('newVisitis')">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="dashboard" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Air Quality
          </div>
          <count-to :start-val=oldquality :end-val=quality :duration="3000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
   

  </el-row>
</template>

<script>
import CountTo from 'vue-count-to'
import { getcurrentSensorData } from '@/api/sensor'
import data from '@/views/pdf/content'
import { set } from 'nprogress'

export default {
  components: {
    CountTo
  },
  data() {
    return {
      time: '',
      temperature: 0,
      humidity: 0,
      light: 0,
      quality: 0,
      oldtemperature: 0,
      oldhumidity: 0,
      oldlight: 0,
      oldquality: 0
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    },
    updateTime() {
      const now = new Date()
      const hours = now.getHours().toString().padStart(2, '0')
      const minutes = now.getMinutes().toString().padStart(2, '0')
      const seconds = now.getSeconds().toString().padStart(2, '0')
      this.time = `${hours}:${minutes}:${seconds}`
    },
    fetchData() {
      this.oldtemperature = this.temperature
      this.oldhumidity = this.humidity
      this.oldlight = this.light
      this.oldquality = this.quality
      getcurrentSensorData().then(response => {
        // console.log(response.data)
        const data = response.data
        console.log(data)
        // const time = data.time.substring(11, 19)
        const temperature = data.temperature
        const humidity = data.humidity
        const light = data.light
        const quality = data.quality
        // this.time = time
        this.temperature = temperature
        this.humidity = humidity
        this.light = light
        this.quality = quality

      }).catch(err => {
        console.log(err)
      })
    }},
  created() {
      this.fetchData()
      setInterval(this.fetchData, 10000)
      setInterval(this.updateTime, 1000)
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>

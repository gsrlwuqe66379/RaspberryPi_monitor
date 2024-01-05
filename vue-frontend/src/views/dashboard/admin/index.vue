<template>
  <div class="dashboard-editor-container">
    <div class="container">
    <streamvideo/>
    <panel-group @handleSetLineChartData="handleSetLineChartData" @handleQueryData="handleQueryData"/>
    </div>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>
      <el-dialog :visible.sync="formVisible" title="query sensor data" width="60%">
      <Filiterform/>
    </el-dialog >
    <el-table :data="tableData">
      <el-table-column prop="time" label="time" width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.time }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="temperature" label="temperature" width="150">
        <template slot-scope="scope">
          <span>{{ scope.row.temperature }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="humidity" label="humidity" width="150">
        <template slot-scope="scope">
          <span>{{ scope.row.humidity }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="light" label="light" width="150">
        <template slot-scope="scope">
          <span>{{ scope.row.light }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="air_quality" label="air_quality" width="150">
        <template slot-scope="scope">
          <span>{{ scope.row.air_quality }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import GithubCorner from '@/components/GithubCorner'
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
import BarChart from './components/BarChart'
import TransactionTable from './components/TransactionTable'
import TodoList from './components/TodoList'
import BoxCard from './components/BoxCard'
import streamvideo from './components/streamvideo'
import Filiterform from './components/Filiterform'
import { getSensorData ,getweatherforecast} from '@/api/sensor'

let lineChartData = {
  airquality: {
    expectedData: [],
    actualData: [],
  },
  temperature: {
    expectedData: [],
    actualData: [],
  },
  humidity: {
    expectedData: [],
    actualData: [],
  },
  light: {
    expectedData: [],
    actualData: [],
  }
}
let tableData = []

export default {
  name: 'DashboardAdmin',
  components: {
    GithubCorner,
    PanelGroup,
    LineChart,
    RaddarChart,
    PieChart,
    BarChart,
    TransactionTable,
    TodoList,
    BoxCard,
    Filiterform,
    streamvideo,
  },
  data() {
    return {
      tableData: tableData,
      formVisible: false,
      lineChartData: lineChartData.temperature,
      time: '',
      temperature: 0,
      humidity: 0,
      light: 0
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type]
    },
    handleQueryData() {
      this.formVisible = !this.formVisible
    },
    fetchdata() {
      getSensorData().then(response => {
        console.log(response)
        this.time = response.data.time
        this.temperature = response.data.temperature
        this.humidity = response.data.humidity
        this.light = response.data.light
        this.air_quality = response.data.air_quality
        console.log(lineChartData)
        lineChartData.temperature.actualData=this.temperature
        lineChartData.humidity.actualData=this.humidity
        lineChartData.light.actualData=this.light
        lineChartData.airquality.actualData=this.air_quality
        for (let index = 0; index < this.time.length; index++) {
          const element = {
            time: this.time[index],
            temperature: this.temperature[index],
            humidity: this.humidity[index],
            light: this.light[index],
            air_quality: this.air_quality[index]
          };
          tableData.push(element)
        }
        
        console.log("123")
        console.log(tableData)
      })
      getweatherforecast().then(response => {
        console.log(response)
        this.temperature = response.data.temperature
        this.humidity = response.data.humidity
        this.light = response.data.light
        this.air_quality = response.data.air_quality
        lineChartData.temperature.expectedData=this.temperature
        lineChartData.humidity.expectedData=this.humidity
        lineChartData.light.expectedData=this.light
        lineChartData.airquality.expectedData=this.air_quality
        console.log(lineChartData)
      })
    }
  },
  created() {
    this.fetchdata()
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;
  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>

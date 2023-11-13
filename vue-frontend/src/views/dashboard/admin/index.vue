<template>
  <div class="dashboard-editor-container">
    <panel-group @handleSetLineChartData="handleSetLineChartData" @handleQueryData="handleQueryData"/>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>
      <el-dialog :visible.sync="formVisible" title="query sensor data" width="60%">

      <Filiterform/>
    </el-dialog >
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
import Filiterform from './components/Filiterform'
import { getSensorData } from '@/api/sensor'

let lineChartData = {
  newVisitis: {
    expectedData: [100, 120, 161, 134, 105, 160, 165],
    actualData: [120, 82, 91, 154, 162, 140, 145],
    predictedData: [110, 82, 91, 154, 162, 140, 145]
  },
  temperature: {
    expectedData: [20, 19, 12, 14, 16, 13, 14],
    actualData: [],
    predictedData:[]
  },
  humidity: {
    expectedData: [80, 60, 40, 45, 65, 75, 80],
    actualData: [],
    predictedData:[]
  },
  light: {
    expectedData: [60, 140, 250, 400, 545, 350, 260],
    actualData: [],
    predictedData:[]
  }
}

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
  },
  data() {
    return {
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
    fetchdata(){
      getSensorData().then(response => {
        this.time = response.data.time
        this.temperature = response.data.temperature
        this.humidity = response.data.humidity
        this.light = response.data.light
        console.log(this.time)
        console.log(lineChartData)
        lineChartData.temperature.actualData=this.temperature
        lineChartData.humidity.actualData=this.humidity
        lineChartData.light.actualData=this.light
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

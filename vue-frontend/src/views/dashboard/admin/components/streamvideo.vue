<template>
    <div>
    <head>
    <title>MJRoBot Lab Live Streaming</title>
    <link rel="stylesheet" href='../static/style.css'/>
  </head>
  <body>
    <h1>实时视频监控窗口</h1>
    <h3><img src="http://127.0.0.1:7778/video_feed" width="70%"></h3>
  </body>
</div>
</template>


<script>
import { getstreamVideo } from '@/api/sensor'


export default {
    data() {
      return {
        videoFeedUrl: 'http://localhost:7778/video_feed',
      }
    },
    created() {
      this.getvideo()
    },
    methods: {
      getvideo(){
       console.log("getvideo")
    }
  }
}

</script>

<style lang="scss" scoped>
body{
	background: whitesmoke;
	color: #2983BB;
	padding:1%;
	text-align: center;
}
</style>
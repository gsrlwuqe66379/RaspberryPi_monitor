<template>
    <div>
    <head>
    <title>MJRoBot Lab Live Streaming</title>
    <link rel="stylesheet" href='../static/style.css'/>
  </head>
  <body>
    <h1>BerryPi Camera Live Streaming</h1>
    <h3><img src="http://localhost:7777/video_feed" width="50%"></h3>
    <hr>
    <p> @2023 Resiberry</p>
  </body>
</div>
</template>


<script>
import { getstreamVideo } from '@/api/sensor'


export default {
    data() {
      return {
        videoFeedUrl: 'http://localhost:7777/video_feed',
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
	background: black;
	color: yellow;
	padding:1%;
	text-align: center;
}
</style>
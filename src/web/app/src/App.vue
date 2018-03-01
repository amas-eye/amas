<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  import init from 'service/initialize'
  export default {
    name: 'app',
    mounted() { //主节点挂载后

      init(this.$store)
      window.onresize = ()=> {
        //窗口调整大小
        init(this.$store)
      }
    }
  }
</script>

<style lang="scss">
  @import './css/style-index.css';
  @import './css/elementReset.scss';
  @import './css/common.scss';
  * {
    margin: 0;
    padding: 0;
  }
  html,
  body {
    /* fonsize预设分辨率为1600 16px */
    font-size: 17.3163px;
  }
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    width: 66.7rem;
    height: 100%;
    overflow-x: hidden;
    /*display:flex;*/
    background: -webkit-linear-gradient(145deg, #2DD7C7 -22%, #c5c0fd 58%, #fdb9c3 122%);
    background: -o-linear-gradient(145deg, #2DD7C7 -22%, #c5c0fd 58%, #fdb9c3 122%);
    background: -moz-linear-gradient(145deg, #2DD7C7 -22%, #c5c0fd 58%, #fdb9c3 122%);
    background: linear-gradient(145deg, #2DD7C7 -22%, #c5c0fd 58%, #fdb9c3 122%);
    /* font-size: 10px; */
    /* background-color: #fff; */
    /* margin-top: 60px; */
  }
</style>

<template>
  <div id="navBarleft">
    <ul>
      <li class="clickable" v-for="(item,index) in navBarleftData" @click="navBarleftClick(item)">
        <i alt="" :class="item.iconImg" :style="item.src==$route.path||item.srcArry.indexOf($route.path)>-1?'color:#fff':'' "></i>
        <p v-show="item.src==$route.path||item.srcArry.indexOf($route.path)>-1" class="barTitle">{{item.navBarleftTitle}}</p>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    name: 'navBarLeft',
    data() {
      return {
        clickIndex: 0, //选中值
        navBarleftData: [ //tab数组
          {
            iconImg: 'icon-survey', //图标
            navBarleftTitle: '总体概况', //名字
            src: '/navBar/survey', //跳转地址
            srcArry: []
          },
          {
            iconImg: 'icon-monitoring',
            navBarleftTitle: '监控',
            src: '/navBar/generalOverview',
            srcArry: [
              '/navBar/generalOverview',
              '/navBar/monitorView/'
            ]
          },
          {
            iconImg: 'icon-warning',
            navBarleftTitle: '告警',
            src: '/navBar/warning',
            srcArry: []
          },
          {
            iconImg: 'icon-collect',
            navBarleftTitle: '采集管理',
            src: '/navBar/collect',
            srcArry: []
          },
        ]
      }
    },
    methods: {
      navBarleftClick: function(item) {
        // this.clickIndex = index
        // console.log(this)
        this.$router.push(item.src)
      }
    }
  }
</script>

<style scoped>
  #navBarleft i {
    font-size: 2.0rem;
    color: #40414e;
  }
  .navBarTitle {
    height: 1.5rem;
  }
  #navBarleft ul {
    padding-top: 1.4rem;
  }
  #navBarleft li {
    /*padding-top:3rem;*/
    margin-bottom: 1.4rem;
  }
  #navBarleft li p {
    line-height: 1.6rem;
    height: 1.6rem;
    font-size: 0.8rem;
    color: #fff;
  }
  .activeClass {
    color: #fff;
  }
</style>

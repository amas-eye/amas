<template>
   <!-- <div v-show="show" class="charts" ref="chart">
  </div>  -->
   <div class="charts" ref="chart">
  </div> 
</template>

<script>
  // 图表组件
  import echarts from 'echarts'
  export default {
    name: 'charts',
    props: {
      option: { //配置
        type: Object,
        default: function() {
          return {}
        }
      },
      show:{
        type:Boolean,
        default:false
      }
    },
    data() {
      return {
        name: 'chart',
        myChart:{},
     
      }
    },
    computed:{
   
    },
    watch: { //嵌套过深的对象无法监听除非深度监听 耗性能不推荐 不知是否是存在数组的问题 最好发新的整个对象过来
      option: function(value) {
        //监听option配置
         console.log(value)
        this.chartreload(value)
      },
      show:function(val){
        // console.log(val)
        //显示时重置大小免得大小有问题
        this.myChart.resize();
      },
      '$store.state.fonsize':function(val){
        //监听全局fonsize 比例变化
        console.log(val)
        this.myChart.resize();
      }
    },
    methods: {
      chartreload: function(option) {
        //重新加载图表
        
        this.myChart.setOption(option);
      }
    },
    // computed:{
    //     chartoption:function(){
    //     return this.option
    //     }
    // },
    mounted() {
      //组件挂载后
      // console.log(this)
       this.myChart = echarts.init(this.$refs.chart);
        this.chartreload(this.option)
    },
    updated() {
      //数据更新后
       console.log(this.option)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .charts {
    width: 100%;
    height: 100%;
  }
</style>

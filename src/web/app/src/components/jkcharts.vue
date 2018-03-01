<template>
  <!-- <div v-show="show" class="charts" ref="chart">
                                                    </div>  -->
  <div class="jkcharts" ref="chart">
  </div>
</template>

<script>
  // 监控的图表组件
  import echarts from 'echarts'
  import http from 'service/myhttp'
  import urls from 'service/url'
  import moment from 'moment'
  import simdate from 'service/simdate'
  export default {
    name: 'jkcharts',
    props: {
      option: { //配置
        type: Object,
        default: function() {
          return {}
        }
      },
      date: { //传入日期时间
        type: Object,
        default: function() {
          return {
            start: simdate.day7_ago(),
            end: simdate.today()
          }
        }
      },
      reloadhz: { //刷新频率
        type: Number,
        default: 0
      },
      show: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        name: 'jkchart',
        myChart: {},
        zbdata: [],
        dataNames: [], //数据名数组
        // dataArry: [], //图表填充数据数组
        timer: null //定时器id
        // ytype:{}, //y轴样式
      }
    },
    computed: {
      // chartwidth: function() {
      //   // 监听图表容器宽
      //   return this.$refs.chart.offsetWidth
      // },
      datetime: function() {
        //日期时间（时间戳）
        return {
          start: moment(this.date.start).format('X'),
          end: moment(this.date.end).format('X')
        }
      },
      chartoption: function() {
        let series = [] //指标图表配置数组
        this.option.xnzbs.forEach((zb, zbindex) => {
          //遍历所有指标配置
          if (zb.tag.length > 0) { //如果有配置分组标签
            zb.tag.forEach((onetag, tagindex) => {
              //遍历指标配置所有分组标签
              let confiname = zb.zbname //配置的数据名（指标加主机）
              confiname = confiname + '(' + onetag.value + ')' //数据名（指标加主机）
              this.zbdata.forEach((item, index) => {
                //遍历指标数据数组(不是一个指标一个数据而是一个指标的一个主机一个数据)
                console.info('数据', item)
                item.forEach((data, dataindex) => {
                  //遍历指标主机数据组
                  let dataname = data.metric //获取的数据名（指标加主机）
                  let hostname = ''
                  if (typeof(data.tags[onetag.key]) != "undefined" && data.tags[onetag.key] != '') { //判断是否分主机名
                    hostname = '(' + data.tags[onetag.key] + ')' //主机名
                  }
                  
                  dataname = dataname + hostname
                  if (confiname == dataname || onetag.value == '*') {
                    this.dataNames.push(dataname) //填充数据名数组
                    //数据指标名等于某指标名 然后导入指标当前配置
                    series.push({
                      name: dataname,
                      type: 'line',
                      itemStyle: {
                        normal: {
                          show: false
                        },
                        emphasis: {
                          show: true
                        },
                      },
                      // symbolSize:0,
                      showSymbol: false,
                      // smooth:true,
                      sampling: 'average',
                      yAxisIndex: zb.yselect == 'right' ? 1 : 0, //y轴位置0左1右
                      // stack: '总量',
                      // areaStyle: {
                      //   normal: {}
                      // },
                      data: data.dps //数据点数据
                    })
                  }
                })
              })
            })
          }
          else{
            //如果没有配置分组标签
            
              //遍历指标配置所有分组标签
              let confiname = zb.zbname //配置的数据名（指标加主机）
              this.zbdata.forEach((item, index) => {
                //遍历指标数据数组(不是一个指标一个数据而是一个指标的一个主机一个数据)
                console.info('数据', item)
                item.forEach((data, dataindex) => {
                  //遍历指标主机数据组
                  let dataname = data.metric //获取的数据名（指标加主机）
                  // let hostname = ''
                  // if (typeof(data.tags[onetag.key]) != "undefined" && data.tags[onetag.key] != '') { //判断是否分主机名
                  //   hostname = '(' + data.tags[onetag.key] + ')' //主机名
                  // }
                  // dataname = dataname + hostname
                  if (confiname==dataname) {
                    //数据指标名等于某指标名 然后导入指标当前配置
                     this.dataNames.push(dataname) //填充数据名数组
                    series.push({
                      name: dataname,
                      type: 'line',
                      itemStyle: {
                        normal: {
                          show: false
                        },
                        emphasis: {
                          show: true
                        },
                      },
                      // symbolSize:0,
                      showSymbol: false,
                      // smooth:true,
                      sampling: 'average',
                      yAxisIndex: zb.yselect == 'right' ? 1 : 0, //y轴位置0左1右
                      // stack: '总量',
                      // areaStyle: {
                      //   normal: {}
                      // },
                      data: data.dps //数据点数据
                    })
                  }
                })
              })
            
          }
        })
        console.log(series)
        return {
          // title: {
          //   text: '堆叠区域图'
          // },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }
            }
          },
          legend: {
            data: this.dataNames
          },
          // toolbox: {
          //   feature: {
          //     saveAsImage: {}
          //   }
          // },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [{
            type: 'time',
            // boundaryGap: false,
          }],
          yAxis: [{
              name: this.option.yconfig.left.type,
              type: 'value'
            },
            {
              name: this.option.yconfig.right.type,
              type: 'value'
            }
          ],
          series: series
        }
      }
    },
    watch: { //嵌套过深的对象无法监听除非深度监听 耗性能不推荐 不知是否是存在数组的问题 最好发新的整个对象过来
      option: function(value) {
        //监听option配置
        // console.log(value)
        this.chartreload()
        //this.getchartdata()
      },
      date: function(value) {
        // 日期时间
        console.log(this.datetime)
        this.chartreload()
      },
      reloadhz: function(val) {
        //刷新频率更改时
        console.log('reloadhz',val)
        this.refresh()
      },
      show: function(val) {
        // console.log(val)
        //显示时重置大小免得大小有问题
        this.myChart.resize()
      },
      '$store.state.fonsize': function(val) {
        //监听全局fonsize 比例变化
        // console.log(val)
        this.myChart.resize();
      }
      // chartwidth: function(val) {
      //   this.myChart.resize();
      // }
    },
    methods: {
      getjkdata: function(data) {
        //获取监控图表数据
        return new Promise((resolve, reject) => {
          http.get(urls.HQJKSJ, data).then(res => {
              resolve(res.data)
            },
            err => {
              reject(err)
            }
          )
        })
      },
      chartreload: function() {
        //重新加载图表
        this.getchartdata(this.option).then(res => {
          //获取图表数据
          this.zbdata = res //一组请求获取的数据
        
          console.info('指标数据', this.zbdata)
          this.zbdata.forEach(item => {
            //遍历请求获取的数据
            item.forEach(data => {
              //遍历数据数量（一个指标可能有多个主机数据）
        
              let onedata = [] //一个数据组
              for (let key in data.dps) {
                if (data.dps.hasOwnProperty(key)) {
                  let value = data.dps[key];
                  //遍历获取key（时间）value(值)
                  let dataitem = [simdate.TMDTime(moment.unix(key)), value] //数据项
                  onedata.push(dataitem) //填充一个数据组
                }
              }
              // console.info('数据',onedata)
              data.dps = onedata //填充数据组
  
            })
          })
          this.myChart.setOption(this.chartoption)
          this.myChart.resize()
        })
      },
      getchartdata: function(option) {
        //获取图表数据
        let xnzbs = option.xnzbs //性能指标
        let reques_arry = [] //请求数组
        xnzbs.forEach((item) => { //遍历查询所有指标
          let tags = ''
          if (item.tag.length > 0) {
            tags = '{' //所有tag组成的对象字符串
            item.tag.forEach((tag, index) => {
              if (tag.key != '') {
                if (index + 1 < item.tag.length) {
                  tags = tags + tag.key + '=' + (tag.value == '' ? '*' : tag.value) + ','
                } else {
                  tags = tags + tag.key + '=' + (tag.value == '' ? '*' : tag.value) + '}'
                }
              }
            })
          }
          let qygz = '' //取样规则
          if (item.qytime != '' && item.qytimed != '' && item.qyfun != '') {
            qygz = '' + item.qytime + item.qytimed + '-' + item.qyfun + ':' //取样规则
            // console.log(item)
          }
          let data = {
            start: this.datetime.start, //开始时间
            end: this.datetime.end, //结束时间
            m: item.aggfun + ':' + qygz + item.zbname + tags //查询规则
          }
          // http.get(urls.HQJKSJ, data).then(res=>{
          //   console.log(res)
          // })
          reques_arry.push(this.getjkdata(data))
        })
        return Promise.all(reques_arry)
      },
      refresh: function() {
        //定时刷新
        if (this.reloadhz) {
          //判断是否有设频率
          // console.log(this.reloadhz)
          if (this.timer) { //判断之前是否设了定时器
            clearInterval(this.timer)
          }
          this.timer = setInterval(() => {
            this.chartreload()
          }, this.reloadhz)
        } else {
          if (this.timer) {
            clearInterval(this.timer)
            this.timer = null
          }
        }
      }
    },
    mounted() {
      //组件挂载后
      let chart = this.$refs.chart
      this.myChart = echarts.init(chart);
      this.chartreload()
      console.info('组件', this)
      //  window.addEventListener("onresize",function(){
      //     this.myChart.resize();
      // } );
      // window.onresize=function(){
      //     this.myChart.resize();
      // }
    },
    updated() {
      //数据更新后
      console.log(this.option)
    },
    destroyed(){
      clearInterval(this.timer)
      this.timer = null;
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .jkcharts {
    width: 100%;
    height: 100%;
  }
</style>

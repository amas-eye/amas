<template>
  <div class="monitorView">
    <!-- 顶部 -->
    <section class="top clearfix">
      <h3 class="fl">{{viewname}}</h3>
      <button class="addChartBtn fr clickable" @click="editView()">添加监控图表</button>
      <button class="lastTimeBtn fr clickable" @click="edit_time()">{{dateTimeString}}</button>
    </section>
    <!-- 顶部 -->
    <!-- 内容 -->
    <section class="main_content">
      <div class="content_bottom" v-for="chart in chartList">
        <!-- 图表 -->
        <div class="tipInfo">
          <div>
            <h4 class="fl">{{chart.title}}</h4>
            <button class="fr clickable" title="添加到概览" @click="addmychart(chart)"><i class="icon-pushToHome"></i></button>
            <button class="fr clickable" title="分享"><i class="icon-share"></i></button>
            <button class="fr clickable" title="切换折线图"><i class="icon-linechart"></i></button>
            <button class="fr clickable" title="设置" @click="editView(chart)"><i class="icon-setting"></i></button>
          </div>
        </div>
        <div class="chart">
          <jkchart :option="chart" :date="datetime" :reloadhz="reloadhz"></jkchart>
        </div>
      </div>
    </section>
    <!-- 内容 -->
    <!-- 新增监控图表 -->
    <div class="chart_box">
      <el-dialog :title="edittype+'监控图表'" :visible.sync="dialogVisible" size="tiny" :before-close="handleClose">
        <div class="chart_content">
          <div class="nav_Box">
            <ul class="nav clearfix">
              <li class="fl clickable" :class="{'active':index===monitoringInfo.navIndex}" @click="monitoringInfo.navIndex = index" v-for="(val,index) in monitoringInfo.navDataList">{{val}}</li>
            </ul>
            <div class="line"></div>
          </div>
          <div class="main_box">
            <!-- 基本信息 -->
            <div class="baseInfo_box" v-show="monitoringInfo.navIndex === 0">
              <div class="title clearfix">
                <p class="left_title fl">标&nbsp;&nbsp;题</p>
                <input class="fl" placeholder="请输入标题" v-model="editChart.nomalinfo.title" type="text">
              </div>
              <!-- 图表类型 -->
              <ul class="chart_type_box clearfix">
                <li class="fl clickable" v-if="chartVal=='折线图'" :class="{'active':editChart.nomalinfo.type===chartVal,'disable':chartVal!='折线图'}" @click="editChart.nomalinfo.type=chartVal" v-for="(chartVal,chartIndex) in monitoringInfo.chartType">{{chartVal}}</li>
                <li class="fl" v-if="chartVal!='折线图'" :class="{'active':editChart.nomalinfo.type===chartVal,'disable':chartVal!='折线图'}" v-for="(chartVal,chartIndex) in monitoringInfo.chartType">{{chartVal}}</li>
              </ul>
              <!-- <div class="tag clearfix">
                                                                                                              <p class="left_title fl">标&nbsp;&nbsp;签</p>
                                                                                                              <button class="fl"><i class="icon-plus2"></i></button>
                                                                                                            </div> -->
              <!-- <ul>
                                                                                                                <li class="clearfix" v-for="(tag_val,tag_index) in 5">
                                                                                                                  <input type="" class="fl" placeholder="请输入标签名" name="">
                                                                                                                  <button class="fl"><i class="icon-delete"></i></button>
                                                                                                                </li>
                                                                                                              </ul> -->
            </div>
            <!-- 性能指标 -->
            <div class="target_box" v-show="monitoringInfo.navIndex === 1">
              <div class="target_content_box" v-for="(indexitem,index) in editChart.pfm_index">
                <button class="indexBtn btn">{{index+1}}</button>
                <button class="deletAllBtn btn clickable" @click="delxnzb" type="button" title="删除"><i class="icon-delete"></i></button>
                <div class="one clearfix">
                  <p class="left_title fl">指标名</p>
                  <el-select @change="zbnameChange(indexitem)" v-model="indexitem.zbname" class="fl target_input ml" placeholder="请选择">
                    <el-option @click="item.tag = [];" v-for="item in zbList" :key="item" :label="item" :value="item">
                    </el-option>
                  </el-select>
                  <p class="left_title fl ml">聚合函数</p>
                  <el-select v-model="indexitem.aggfun" class="fl func_input ml" placeholder="请选择">
                    <el-option  v-for="item in funList" :key="item" :label="item" :value="item">
                    </el-option>
                  </el-select>
                  <p class="left_title fl ml">序列名称</p>
                  <p class="right_title fl ml"><input class="text" v-model="indexitem.xlname" placeholder="序列名称" type="text" /></p>
                </div>
                <div class="two clearfix">
                  <p class="left_title fl">取样时间</p>
                  <p class="right_title fl ml"><input class="text" v-model="indexitem.qytime" placeholder="时间" type="text" /></p>
                  <el-select v-model="indexitem.qytimed" class="fl day_input ml" placeholder="请选择">
                    <el-option v-for="item in timeunits" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
                  <p class="left_title fl ml">取样函数</p>
                  <el-select v-model="indexitem.qyfun" class="fl func_input ml" placeholder="请选择">
                    <el-option v-for="item in funList" :key="item" :label="item" :value="item">
                    </el-option>
                  </el-select>
                  <p class="left_title fl ml">Y轴</p>
                  <el-select v-model="indexitem.yselect" class="fl func_input ml" placeholder="请选择">
                    <el-option v-for="item in yselects" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
                </div>
                <div class="three clearfix">
                  <p class="left_title fl">TAG</p>
                  <button class="ml fl btn clickable" @click="addtag(indexitem.tag)" title="添加"><i class="icon-plus"></i></button>
                </div>
                <ul>
                  <li class="clearfix" style="margin-bottom:0.25rem;" v-for="(tag,index) in indexitem.tag">
                    <el-select  v-model="tag.key" @change="tagkeychoose(indexitem,tag)" class="fl key_input" placeholder="请选择">
                      <el-option @click="tag.value = '*';" v-for="item in indexitem.tagkeyList" :key="item" :label="item" :value="item">
                      </el-option>
                    </el-select>
                    <el-select v-model="tag.value" class="fl value_input ml" placeholder="请选择">
                      <el-option :key="'*'" :label="'所有'" :value="'*'">
                      </el-option>
                      <el-option v-for="item in tag.tagvalList" :key="item" :label="item" :value="item">
                      </el-option>
                    </el-select>
                    <button class="ml btn fl" type="button" @click="deltag(indexitem.tag,index)" title="删除"><i class="icon-delete"></i></button>
                  </li>
                </ul>
              </div>
              <button class="addBtn clickable" @click="addxnzb">＋新加指标</button>
            </div>
            <!-- 性能指标 -->
            <!-- 图表样式 -->
            <div class="charstyle_box" v-show="monitoringInfo.navIndex === 2">
              <h3>Y轴设置</h3>
              <div class="clearfix top">
                <p class="left_title fl">左Y轴</p>
                <p class="left_title fl ml">单位</p>
                <el-select v-model="editChart.ystyle.left.type" class="fl key_input ml" placeholder="请选择">
                  <el-option v-for="item in yconfig_types" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
                <el-select v-model="editChart.ystyle.left.unit" class="fl value_input ml" placeholder="请选择">
                  <el-option v-for="item in yconfig_left_units" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </div>
              <div class="clearfix">
                <p class="left_title fl">右Y轴</p>
                <p class="left_title fl ml">单位</p>
                <el-select v-model="editChart.ystyle.right.type" class="fl key_input ml" placeholder="请选择">
                  <el-option v-for="item in yconfig_types" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
                <el-select v-model="editChart.ystyle.right.unit" class="fl value_input ml" placeholder="请选择">
                  <el-option v-for="item in yconfig_right_units" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </div>
            </div>
            <!-- 图表样式 -->
          </div>
        </div>
        <div class="bottom_btnBox">
          <button class="sureBtn clickable" v-if="edittype=='新增'" type="button" @click="addchart">确定</button>
          <button class="sureBtn clickable" v-if="edittype=='编辑'" type="button" @click="editchart">确定</button>
          <button class="cancleBtn clickable" type="button" @click="dialogVisible = false">取消</button>
        </div>
      </el-dialog>
    </div>
    <!-- 新增监控图表 -->

    <!--编辑时间弹出框-->
    <div class="time_edit_box">
      <div class="time_edit_wrapper" v-show="editTimeShow" @click.self="editTimeShow=!editTimeShow">
      <!--编辑时间-->
        <div  class="edit_time">
          <div class="btnBox selfTime">
            <!--快捷时间选择-->
            <button v-for="item in shelfTimes" @click="shelfTimeSelect(item.label,item.value);updatedatetimeconfigs();" class="clickable" type="button">{{item.label}}</button>
            <button @click="showdeftime=!showdeftime;showdeftimeClick()" class="clickable definebtn" type="button">自定义</button>
          </div>
          <div v-show="showdeftime" class="selfDefined">
            <!-- 自定义时间窗口 -->
            <div class="from">
              <el-date-picker v-model="definedTime.start" type="datetime" placeholder="开始时间">
              </el-date-picker>
              <el-date-picker v-model="definedTime.end" type="datetime" placeholder="结束时间">
              </el-date-picker>
              <el-select v-model="definedTime.reloadhz" class="hzselect" placeholder="请选择">
                <el-option v-for="item in hzArry" :key="item.label" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </div>
            <div class="btnBox toolbuttons">
              <button @click="seleDefinedTime();updatedatetimeconfigs();" class="clickable ok" type="button">确定</button>
              <button @click="editTimeClose" class="clickable cancel" type="button">取消</button>
            </div>
          </div>
        </div>
      <!--编辑时间-->        
      </div>
    </div>
    <!--编辑时间弹出框-->
  </div>
</template>
<script>
  import http from 'service/myhttp'
  import urls from 'service/url'
  import jkchart from 'components/jkcharts'
  import simdate from 'service/simdate'
  export default {
    name: 'monitorView',
    components: {
      jkchart
    },
    data() {
      return {
        editTimeShow: false, //时间编辑弹窗显示
        shelfTimes: [ //快捷时间数据数组
          {
            label: '5分钟',
            value: simdate.min5_ago()
          },
          {
            label: '10分钟',
            value: simdate.min10_ago()
          },
          {
            label: '30分钟',
            value: simdate.min30_ago()
          },
          {
            label: '1小时',
            value: simdate.hour1_ago()
          },
          {
            label: '6小时',
            value: simdate.hour6_ago()
          },
          {
            label: '12小时',
            value: simdate.hour12_ago()
          },
          {
            label: '1天',
            value: simdate.day1_ago()
          },
          {
            label: '7天',
            value: simdate.day7_ago()
          },
          {
            label: '15天',
            value: simdate.day15_ago()
          },
        ],
        datetime: { //时间选择
          start: simdate.day7_ago(),
          end: simdate.today()
        },
        showdeftime: false, //自定义时间显示
        definedTime: { //自定义时间
          start: simdate.day7_ago(),
          end: simdate.today(),
          reloadhz:0
        },
        dateTimeString: '最新7天', //日期时间显示字符
        reloadhz: 0, //刷新频率
        hzArry: [ //频率数组
          {
            label: 'OFF',
            value: 0
          },
          {
            label: '5秒',
            value: 5000
          },
          {
            label: '30秒',
            value: 30000
          },
          {
            label: '1分钟',
            value: 60000
          },
          {
            label: '5分钟',
            value: 300000
          },
          {
            label: '30分钟',
            value: 1800000
          }
        ],
        timeunits: [{ //时间单位选择
            label: '秒',
            value: 's'
          },
          {
            label: '分钟',
            value: 'm'
          },
          {
            label: '小时',
            value: 'h'
          },
          {
            label: '天',
            value: 'd'
          },
          {
            label: '周',
            value: 'w'
          },
          {
            label: '月',
            value: 'n'
          },
          {
            label: '年',
            value: 'y'
          }
        ], //时间单位数组
        yselects: [ //y轴选择
          {
            label: '左y轴',
            value: 'left'
          },
          {
            label: '右y轴',
            value: 'right'
          }
        ],
        yconfig_types: ['数值', '数据', '比例', '时间'], //y轴配置（类型）
        viewid: '', //所属视图id
        viewname: '',
        zbList: [], //指标名列表
        funList: [], //函数接口地址数组
        value: '',
        dialogVisible: false, //监控图表显示隐藏
        monitoringInfo: { //监控数据
          navIndex: 0,
          navDataList: ['基本信息', '性能指标', '图表式样'],
          chartType: ['折线图', '柱图', '热力图', '散点图', '饼图', '雷达图', '树图', '表格'],
          chartTypeIndex: 0
        },
        edittype: '新增', //编辑窗口状态
        editChart: {
          //编辑图表（配置数据）
          nomalinfo: {
            //基础信息
            title: '', //图表标题
            type: '折线图', //图表类型
          },
          pfm_index: [
            //性能指标
            {
              zbname: '', //指标名称
              xlname: '', //序列名称
              qytime: '', //取样时间
              qytimed: '', //取样时间单位
              aggfun: '', //聚合函数
              qyfun: '', //取样函数
              yselect: '', //y轴选择 （左或右）
              tagkeyList: [], //tagkey 数组
              tag: [
                //   { //标签
                //   key: '', //键值
                //   value: '', //值
                //   tagvalList: [], //tagvaule 数组
                // }
              ],
            }
          ],
          ystyle: {
            //y轴样式配置
            left: {
              //左边y轴
              type: '', //类型
              unit: '' //单位
            },
            right: {
              //右边y轴
              type: '', //类型
              unit: '' //单位
            }
          }
        },
        chartList: [] //图表（配置）列表
      }
    },
    computed: {
      yconfig_left_units: function() {
        //左边y轴单位（类型）
        let data = []
        switch (this.editChart.ystyle.left.type) {
          case '数值':
            data = ['个', '千', '万', '千万']
            break;
          case '数据':
            data = ['K(KiloBytes)', 'M(MegaBytes)', 'G(GigaBytes)']
            break;
          case '比例':
            data = ['十分之几', '百分之几', '千分之几', '万分之几']
            break;
          case '时间':
            data = ['秒', '分钟', '小时']
            break;
          default:
            break;
        }
        return data
      },
      yconfig_right_units: function() {
        //右边y轴单位（类型）
        let data = []
        switch (this.editChart.ystyle.right.type) {
          case '数值':
            data = ['个', '千', '万', '千万']
            break;
          case '数据':
            data = ['M(MegaBytes)', 'K(KiloBytes)', 'M(MegaBytes)', 'G(GigaBytes)']
            break;
          case '比例':
            data = ['十分之几', '百分之几', '千分之几', '万分之几']
            break;
          case '时间':
            data = ['秒', '分钟', '小时']
            break;
          default:
            break;
        }
        return data
      },
    },
    mounted() {
      //挂载时
      this.viewid = this.$route.query.viewid
      this.viewname = this.$route.query.name
      this.getdatetimeconfigs().then(data => {
        this.searchart()
      })
      http.get(urls.LQZBMLB, { //拉取指标名列表
        type: 'metrics',
        max: 99999
      }).then(res => {
        let data = res.data
        this.zbList = data
        // console.log(data)
      })
      http.get(urls.JHHS).then(res => { //聚合函数取样函数
        let data = res.data
        this.funList = data
        // console.log(data)
      })
    },
    methods: {
      getdatetimeconfigs: function() {
        //获取视图数据的时间间隔配置
        return new Promise((resolve, reject) => {
          http.get(urls.HQSTSJPZ, {
            viewid: this.viewid
          }).then(res => {
            // console.info('获取视图数据的时间间隔配置', res)
            let data = []
            if (res.data.length > 0) { //如果有数据
              data = res.data[0]
              let dataoption = {
                start: data.start,
                end: data.end,
              }
              this.dateTimeString=data.datetext
              this.definedTime = Object.assign({}, {
                start: data.start,
                end: data.end,
              },{'reloadhz':data.reloadhz})
              this.datetime = dataoption
              this.reloadhz = data.reloadhz
            }
            resolve(data)
          }, err => {
            reject(err)
          })
        })
      },
      updatedatetimeconfigs: function() {
        //更新视图数据的时间间隔配置
        return new Promise((resolve, reject) => {
          http.post(urls.GXSTSJPZ, {
            viewid: this.viewid, //视图id
            datatimeconfig: {
              viewid: this.viewid, //视图id
              start: this.datetime.start, //开始时间
              end: this.datetime.end, //结束时间
              datetext:this.dateTimeString, //时间描述文字
              reloadhz: this.reloadhz //刷新频率
            }
          }).then(res => {
            // console.info('更新视图数据的时间间隔配置', res)
            resolve(res.data)
            this.$message({
              showClose: true,
              message: '操作成功',
              type: 'success'
            })
          }, err => {
            reject(err)
          })
        })
      },
      gettagkey: function(item) {
        //获取tag key
        return new Promise((resolve, reject) => {
          http.get(urls.LQTAGKEY, { //拉取TAG的key
            period: '10m-ago', //时间范围
            metric: 'sum:' + item.zbname,
          }).then(
            res => {
              let data = res.data.data
              // console.info('tagkey数据',data)
              item.tagkeyList = data[0].aggregateTags
              resolve(res)
            }, err => {
              reject(err)
            })
        })
      },
      gettagvalue: function(item, tag) {
        //获取tag value
        http.get(urls.LQTAGVAL, { //拉取TAG的key/value
          start: '10m-ago', //时间范围
          m: 'sum:' + item.zbname + '{' + tag.key + '=*}',
          // max: 99999
        }).then(res => {
          tag.tagvalList = [] //数据库不可能记录这个列表所以要初始化
          let data = res.data
          data.forEach(onedata => {
            //遍历数据 （数据库接口奇葩）
            // console.info('tag数据', onedata)
            tag.tagvalList.push(onedata.tags[tag.key])
          })
          // console.log(data)
        })
      },
      zbnameChange: function(item) {
        //指标名更改(element组件 主动改数据也触发change,只要数据更改就触发)
        // console.info('指标名更改', item)
        this.gettagkey(item)
        // item.tag = [] //标签数组复位
      },
      tagkeychoose: function(item, tag) {
        //分组标签选择
        //  console.info('分组标签选择', tag)
       // tag.value = '*' //标签值复位
        this.gettagvalue(item, tag)
      },
      editView: function(chart) {
        //设置图表
        // console.info('编辑配置',chart.xnzbs)
        if (chart) {
          //编辑视图
          this.edittype = '编辑'
          this.editChart.nomalinfo._id = chart._id
          this.editChart.nomalinfo.title = chart.title
          this.editChart.nomalinfo.type = chart.type
          // this.editChart.pfm_index = chart.xnzbs
          this.editChart.ystyle = chart.yconfig
          // console.info('指标数组', this.editChart)
          let gettagvalues = [] //获取标签值请求数组
          chart.xnzbs.forEach((item) => {
            //遍历指标数组
            if (item.zbname != null && item.zbname != '') {
              gettagvalues.push(this.gettagkey(item))
              item.tag.forEach((onetag) => {
                if (onetag.key != null && onetag.key != '') {
                  // console.info('其中一个tag', onetag)
                  gettagvalues.push(this.gettagvalue(item, onetag))
                }
              })
            }
          })
          Promise.all(gettagvalues).then(datas => {
            this.editChart.pfm_index = chart.xnzbs
            
          })
          // console.log(chart)
        } else {
          //新增视图
          this.edittype = '新增'
          this.editChart = {
            //编辑图表（配置数据）
            nomalinfo: {
              //基础信息
              title: '', //图表标题
              type: '折线图', //图表类型
            },
            pfm_index: [
              //性能指标
              {
                zbname: '', //指标名称
                xlname: '', //序列名称
                qytime: '', //取样时间
                qytimed: '', //取样时间单位
                aggfun: '', //聚合函数
                qyfun: '', //取样函数
                yselect: '', //y轴选择 （左或右）
                tagkeyList: [], //tagkey 数组
                tag: [
                  //   { //标签
                  //   key: '', //键值
                  //   value: '' //值
                  // }
                ],
              }
            ],
            ystyle: {
              //y轴样式配置
              left: {
                //左边y轴
                type: '', //类型
                unit: '' //单位
              },
              right: {
                //右边y轴
                type: '', //类型
                unit: '' //单位
              }
            }
          }
        }
        this.dialogVisible = true;
      },
      addmychart: function(chart) {
        //新增自定义概览图表
        http.post(urls.XZZDYGLTB, {
          id: chart._id
        }).then(res => {
          let data = res.data
          this.$message({
              showClose: true,
              message: '操作成功',
              type: 'success'
            })
        })
      },
      shelfTimeSelect: function(label, value) {
        //快捷时间选择
        this.datetime = {
          start: value,
          end: simdate.todayTime()
        }
        this.dateTimeString = '最新' + label
        this.editTimeClose()
      },
      seleDefinedTime: function() {
        //自定义时间选择
        this.datetime = {
          start: this.definedTime.start,
          end: this.definedTime.end
        }
        this.reloadhz = this.definedTime.reloadhz;
        this.dateTimeString = '开始：' + simdate.TMDTime(this.datetime.start) + ' 结束：' + simdate.TMDTime(this.datetime.end)
        this.editTimeClose()
      },
      edit_time: function() {
        //编辑时间
        this.editTimeShow = !this.editTimeShow
        this.showdeftime = false
      },
      showdeftimeClick:function(){ //自定义按钮点击事件
        if (this.showdeftime) {
          this.definedTime = Object.assign({}, this.datetime,{'reloadhz':this.reloadhz});
        }
        
      },
      editTimeClose: function() {
        this.editTimeShow = false
      },
      handleClose: function() {
        this.dialogVisible = false;
      },
      addxnzb: function() {
        //添加性能指标
        this.editChart.pfm_index.push({
          zbname: '', //指标名称
          xlname: '', //序列名称
          qytime: '', //取样时间
          qytimed: '', //取样时间单位
          aggfun: '', //聚合函数
          qyfun: '', //取样函数
          yselect: '', //y轴选择 （左或右）
          tag: [
            //   { //标签
            //   key: '', //键值
            //   value: '' //值
            // }
          ],
        })
      },
      delxnzb: function(index) {
        //删除性能指标
        this.editChart.pfm_index.splice(index, 1)
      },
      addtag: function(tags) {
        //添加标签
        tags.push({ //标签
          key: '', //键值
          value: '*', //值
          tagvalList: [] //根据tag改变的tagvalue选择数组
        })
      },
      deltag: function(tags, index) {
        //删除标签
        tags.splice(index, 1)
      },
      reload: function() {
        //重新
      },
      addchart: function() {
        //添加图表
        let newoption = Object.assign({}, this.editChart) //新图表数据 （对象深拷贝）（发送前处理掉数据库不要的数据） 
        newoption.pfm_index.forEach(item => {
          delete(item.tagkeyList)
          item.tag.forEach(tag => {
            delete(tag.tagvalList)
          })
        })
        http.post(urls.XZSTTB, {
          viewid: this.viewid,
          option: newoption
        }).then(res => {
          // let data = res.data
          // this.tagkeyList = data
          // console.log(data)
          this.searchart()
          this.dialogVisible = false
          this.$message({
              showClose: true,
              message: '操作成功',
              type: 'success'
            })
        })
      },
      editchart: function() {
        //编辑图表
        let newoption = Object.assign({}, this.editChart) //新图表数据 （对象深拷贝）（发送前处理掉数据库不要的数据） 
        newoption.pfm_index.forEach(item => {
          delete(item.tagkeyList)
          item.tag.forEach(tag => {
            delete(tag.tagvalList)
          })
        })
        http.post(urls.BJSTTB, {
          option: newoption
        }).then(res => {
          // let data = res.data
          // this.tagkeyList = data
          // console.log(data)
          this.searchart()
          this.dialogVisible = false
          this.$message({
              showClose: true,
              message: '操作成功',
              type: 'success'
            })
        })
      },
      searchart: function() {
        //查询图表配置数据
        http.get(urls.CXSTTB, {
          viewid: this.viewid,
        }).then(res => {
          let data = res.data
          // console.info('图表数据', data)
          this.chartList = data
          // console.info('图表数据', data)
        })
      }
    }
  }
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  .top {
    $topFontSize: 0.9rem;
    h3 {
      font-size: $topFontSize;
      color: #414250;
      height: 2rem;
      line-height: 2rem;
    }
    button {
      height: 2rem;
      line-height: 2rem;
      text-align: center;
      color: white;
      border-radius: 3px;
      font-size: $topFontSize;
    }
    .lastTimeBtn {
      background-color: #5182d5;
      margin-right: 0.5rem;
      /* width: 7.2rem; */
      padding: 0rem 1rem;
    }
    .addChartBtn {
      width: 6.4rem;
      background-color: #53c0ba;
    }
  }
  .chart {
    height: 14.5rem;
    background-color: rgba(102, 102, 102, 0.3);
  }
  .main_content {
    margin-top: 0.5rem;
    color: white;
    .tipInfo {
      background-color: rgba(12, 17, 37, 0.3);
      padding: 0 1rem;
      >div {
        height: 1.8rem;
        line-height: 1.8rem;
        box-sizing: border-box;
        border-bottom: 1px solid #0c1125;
        button {
          font-size: 1.1rem;
          color: white;
          margin-top: 0.35rem;
          margin-left: 0.6rem;
          background-color: transparent;
        }
      }
    }
    .content_top {
      .left {
        width: 30.3rem;
        .chart {
          height: 14.5rem; // background-color: yellow;
        }
      }
      .right {
        width: 30.0rem;
        .chart {
          height: 14.5rem; // background-color: yellow;
        }
      }
    }
    .content_bottom {
      margin-top: 0.5rem;
      .chart {
        height: 20rem; // height: 41.2rem; // background-color: yellow;
      }
    }
  }
  .text {
    background: transparent;
    width: 100%;
    margin: 0; // padding-left: 0 !important;
  }
  .text::-webkit-input-placeholder {
    color: #808b96;
  }
  /*编辑时间*/
  .edit_time {
    position: absolute;
    width: 35.2rem;
    right: 7.5rem;
    z-index: 2;
    top: 6.5rem;
    background: rgba(0, 0, 0, 0.8);
    padding: 0.6rem;
    border-radius: 6px;
  }
  .edit_time .btnBox {
    display: flex
  }
  .edit_time .btnBox button {
    height: 1.5rem;
    padding: 0rem 0.5rem;
    line-height: 1.5rem;
    text-align: center;
    color: white;
    border-radius: 2px;
    font-size: 0.9rem;
    background: #41404E;
  }
  .edit_time .selfTime {
    /*快捷时间选择*/
    justify-content: space-between;
  }
  .edit_time .selfDefined .from {
    margin: 0.5rem 0;
    padding: 1rem 0;
    border-top: 1px solid #4168A7;
  }
  .edit_time .toolbuttons {
    display: flex;
    justify-content: center;
  }
  .edit_time .toolbuttons button {
    margin: 0 1rem 0.5rem 1rem;
    height: 2rem;
    width: 6rem;
  }
  .edit_time .definebtn {
    /*自定义按钮*/
    background: #4F82D3 !important;
  }
  .edit_time .ok {
    /*确定取消*/
    background: #0fa3c5 !important;
  }
  .edit_time .cancel {
    /*确定取消*/
    color: white;
    box-sizing: border-box;
    border: 1px solid #0fa3c5;
    background-color: transparent;
  }
  .time_edit_box {
    .time_edit_wrapper {
      z-index: 1001;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      position: fixed;
      overflow: auto;
      margin: 0;
      background-color: rgba(0, 0, 0, 0.5);

    }
  }
</style>

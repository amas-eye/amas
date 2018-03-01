<template>
    <!-- 总体概况 -->
    <div class="survey">
        <div class="title">
            基本指标概况
        </div>
        <div class="charts">
            <div class="chart chart25">
                <!-- 总体监控度评分 -->
                <charts style="height: 10.55rem" :option="a"></charts>
            </div>
            <div class="chart chart25">
                <!-- 主机信息总体 -->
                <div class="head left">主机</div>
                <charts style="height: 10.55rem" :option="b"></charts>
            </div>
            <div class="chart chart25">
                <!-- 告警信息总体 -->
                <div class="head left">告警</div>
                <div class="ztgj">
                    <div class="date">
                        <div class="item">{{cdata.alerts}}<span style="font-size:0.7rem;">条</span></div>
                        <div class="item">{{cdata.produce_total}}<span style="font-size:0.7rem;">条</span></div>
                        <div class="item">{{cdata.canel_total}}<span style="font-size:0.7rem;">条</span></div>
                    </div>
                    <div class="datename">
                        <div class="item">现有告警</div>
                        <div class="item">告警产生数</div>
                        <div class="item">告警撤销数</div>
                    </div>
                    <img class="bg" src="../img/ztgj.png" />
                </div>
            </div>
            <div class="chart chart25">
                <!-- 指标信息 -->
                <div class="head left">指标</div>
                <div class="indicator">
                    <!-- 指标 -->
                    <div class="count">{{ this.ddata.metrics }}<span class="unit">个</span></div>
                    <div class="label">
                        <span class="name">正常</span>
                        <div class="processbg">
                            <div :style="{width:this.ddata.normal/this.ddata.metrics*100+'%'}" style="background: #03eeff;" class="process"></div>
                        </div>
                        <span class="count">{{ this.ddata.normal }}</span>
                    </div>
                    <div class="label">
                        <span class="name">异常</span>
                        <div class="processbg">
                            <div :style="{width:this.ddata.error/this.ddata.metrics*100+'%'}" style="background: #ff839a;" class="process"></div>
                        </div>
                        <span class="count">{{ this.ddata.error }}</span>
                    </div>
                </div>
            </div>
            <div class="chart chart100">
                <!-- 告警趋势 -->
                <div class="head center">告警趋势</div>
                <charts style="height: 12.7rem" :option="e"></charts>
            </div>
            <div class="chart chart50 userat">
                <!-- 利用率top5 -->
                <div class="head center">利用率 Top5 统计</div>
                <div class="tabs">
                    <div v-for="item in useRatRankTypes" :key="item.label" :style="{color:(useRatRankType==item.label?item.color.use:'')}" @click="useRatRankType=item.label" :class="{active:useRatRankType==item.label}" class="tab clickable">
                        {{item.label}}
                    </div>
                </div>
                <div v-show="useRatRankType==item.label" :key="item.label" v-for="item in useRatRankTypes" class="rank ">
                    <!-- 指标 -->
                    <div :key="data.host" v-for="data in fdata[getTopType(item.label)]" class="label">
                        <span class="name">{{ data.host }}</span>
                        <div class="processbg">
                            <div :style="{background:(useRatRankType==item.label?item.color.use:''),width:''+data.per+'%'}" class="process"></div>
                        </div>
                    </div>
                    <div class="scales">
                        <span class="item" :key="scale" v-for="scale in useRatScales">{{scale}}</span>
                    </div>
                </div>
            </div>
            <div class="chart chart50">
                <!-- 基础资源使用量 -->
                <div class="head center">基础资源使用量</div>
                <div class="resourceUse">
                    <charts style="width:33.33%;height: 14.35rem;float:left;" v-for="item in g" :option="item"></charts>
                </div>
            </div>
            <div class="chart chart50">
                <!-- 网络流入流出趋势 -->
                <div class="head center">网络流入流出趋势</div>
                <charts style="height: 14.35rem;" :option="h"></charts>
            </div>
            <div class="chart chart50 flow">
                <!-- 网络流入流出top5统计 -->
                <div class="head center">网络流入流出 top5 统计</div>
                <div class="tabs">
                    <div v-for="item in flowTypes" :key="item.label" @click="flowType=item.label" :style="{color:flowType==item.label?item.color:''}" :class="{active:flowType==item.label}" class="tab clickable">
                        {{item.label}}
                    </div>
                </div>
                <div v-show="flowType==item.label" :key="item.label" v-for="item in flowTypes" class="rank ">
                    <!-- 指标 -->
                    <div :key="data.host" v-for="data in ydata[getTopType(item.label)]" class="label">
                        <span class="name">{{data.host}}</span>
                        <div class="processbg">
                            <div :style="{background:flowType==item.label?item.color:'',width:''+data.per+'%'}" class="process"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="title">
            大数据指标概览
        </div>
        <div class="charts">
            <div :key="item._id" v-for="(item,index) in mycharts" class="chart chart50">
                <div class="head center">{{item.chart.title}}<span @click="remove_mychart(item.chart,index)" class="close clickable" title="删除">x</span></div>
                <jkchart :option="item.chart" style="height: 14.35rem;"></jkchart>
            </div>
        </div>
    </div>
</template>
<script>
    import http from 'service/myhttp'
    import urls from 'service/url'
    import pageIndicator from 'components/pageIndicator' //分页器
    import simdate from 'service/simdate'
    import charts from 'components/charts' //图表组件
    import jkchart from 'components/jkcharts' //监控图表组件
    export default {
        name: 'survey',
        components: {
            pageIndicator,
            charts,
            jkchart
        },
        data() {
            return {
                useRatMax: 100, //利用率最大值
                topMax: {}, //排名最大值
                useRatRankType: 'CPU', //利用率排名类型 
                useRatRankTypes: [ //利用率排名类型数组
                    {
                        label: 'CPU',
                        color: {
                            use: '#03eeff',
                            sum: '#659dbf'
                        }
                    },
                    {
                        label: '内 存',
                        color: {
                            use: '#f4dca6',
                            sum: '#9f9b92'
                        }
                    },
                    {
                        label: '硬 盘',
                        color: {
                            use: '#feb9d5',
                            sum: '#a290b2'
                        }
                    }
                ],
                flowType: '流 入',
                flowTypes: [ //流量类型数组
                    {
                        label: '流 入',
                        color: '#625fc7'
                    },
                    {
                        label: '流 出',
                        color: '#12cfd1',
                    }
                ],
                adata: {} //总体监控度评分 
                ,
                bdata: { //主机信息总体
                },
                cdata: { //告警信息总体
                },
                ddata: { //指标信息
                },
                edata: { //告警趋势 
                },
                fdata: { //利用率top5 
                },
                gdata: null, //基础资源使用量 ,
                hdata: { //网络流入流出趋势 
                },
                ydata: { //络流入流出top5统计
                },
                mycharts: [] //所有自定义概况图表
            }
        },
        computed: {
            useRatScales: function() {
                //利用率
                let scaleCount = 10 //刻度数
                let size = parseInt(this.useRatMax / scaleCount) //单位刻度大小
                let data = []
                for (let i = 0; i < scaleCount + 1; i++) {
                    data.push(i * size)
                }
                // console.log(data)
                return data
            },
            a: function(params) { //总体监控度评分 
                return {
                    tooltip: {
                        formatter: "{a} <br/>{b} : {c}分"
                    },
                    series: [{
                        title: {
                            show: false,
                            textStyle: {
                                fontWeight: 'bolder',
                                fontSize: 20,
                                color: '#fff',
                                shadowColor: '#fff',
                                shadowBlur: 10
                            }
                        },
                        name: '健康度',
                        type: 'gauge', //仪表盘
                        center: ['50%', '60%'],
                        radius: '90%',
                        startAngle: 210,
                        endAngle: -30,
                        axisLine: { // 坐标轴线
                            lineStyle: { // 属性lineStyle控制线条样式
                                color: [
                                    [0.2, '#d03a53'],
                                    [0.8, '#0373c6'],
                                    [1, '#04ff8b']
                                ],
                                width: 3,
                                // shadowColor: '#fff', //默认透明
                                // shadowBlur: 10
                            }
                        },
                        axisLabel: { // 坐标轴小标记
                            show: false,
                            textStyle: { // 属性lineStyle控制线条样式
                                fontWeight: 'bolder',
                                color: '#fff',
                                // shadowColor: '#fff', //默认透明
                                // shadowBlur: 10
                            }
                        },
                        axisTick: { // 坐标轴小标记
                            length: 15, // 属性length控制线长
                            splitNumber: 10,
                            lineStyle: { // 属性lineStyle控制线条样式
                                color: 'auto',
                                // shadowColor: '#fff', //默认透明
                                // shadowBlur: 10
                            }
                        },
                        splitLine: { // 分隔线
                            length: 25, // 属性length控制线长
                            lineStyle: { // 属性lineStyle（详见lineStyle）控制线条样式
                                width: 3,
                                color: '#fff',
                                // shadowColor: '#fff', //默认透明
                                // shadowBlur: 10
                            }
                        },
                        pointer: {
                            show: true,
                            length: '80%',
                            width: 8,
                        },
                        itemStyle: {
                            normal: {
                                color: '#fff',
                                borderColor: '#fff',
                                borderWidth: 0,
                                borderType: 'solid',
                            }
                        },
                        detail: {
                            show: true,
                            borderColor: '#fff',
                            shadowColor: '#fff',
                            textStyle: {
                                fontWeight: 'bolder',
                                color: '#fff'
                            },
                            formatter: '健康度\n{value}分'
                        },
                        data: [{
                            value: this.adata.score,
                            name: '健康度'
                        }]
                    }]
                }
            },
            b: function(params) { //主机 
                return {
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b}: {c} ({d}%)"
                    },
                    legend: {
                        orient: 'vertical',
                        // x: 'center',
                        // y: 'bottom',
                        // align:'right',
                        right: '4%',
                        bottom: '4%',
                        textStyle: {
                            color: '#fff',
                            fontSize: '14',
                        },
                        formatter: function(name) {
                            return name
                        },
                        data: ['正常', '异常', '关闭']
                    },
                    graphic: {
                        type: 'text',
                        right: '50%',
                        top: '39%',
                        style: {
                            text: this.bdata.hosts,
                            fill: '#fff',
                            font: '3.5em "STHeiti", sans-serif'
                        }
                    },
                    series: [{
                        name: '访问来源',
                        type: 'pie',
                        center: ['47%', '45%'],
                        radius: ['50%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            normal: {
                                show: false,
                                position: 'outside',
                                formatter: '{c}台',
                            },
                            emphasis: {
                                show: true,
                                // borderRadiu:100,
                                textStyle: {
                                    fontSize: '18',
                                    color: '#fff',
                                    fontWeight: 'bold'
                                }
                            }
                        },
                        labelLine: {
                            normal: {
                                show: false,
                                length: 9,
                                length2: 9,
                            }
                        },
                        data: [{
                                value: this.bdata.hosts_normal,
                                name: '正常',
                                itemStyle: {
                                    normal: {
                                        color: '#03eeff'
                                    }
                                },
                            },
                            {
                                value: this.bdata.hosts_error,
                                name: '异常',
                                itemStyle: {
                                    normal: {
                                        color: '#e68494'
                                    }
                                }
                            },
                            {
                                value: this.bdata.hosts_closed,
                                name: '关闭',
                                itemStyle: {
                                    normal: {
                                        color: '#d6e2ed'
                                    }
                                }
                            }
                        ]
                    }]
                }
            },
            c: function() { //告警信息总体 
                return {}
            },
            d: function() { //指标信息
                return {}
            },
            e: function() { //告警趋势 
                return {
                    //近一小时客流趋势chart图配置
                    title: { //图表标题
                        // text: '近一小时客流趋势',
                        // subtext: "客流量(人)",
                        textStyle: {
                            fontFamily: '微软雅黑',
                            fontWeight: 'normal', //标题颜色
                            fontSize: 17,
                            color: '#73C5FA'
                        },
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    grid: { //图表在div的布局控制
                        top: '15%',
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [{ //X轴样式
                        type: 'category',
                        boundaryGap: false,
                        axisLine: {
                            show: false
                        },
                        axisTick: false,
                        axisLabel: {
                            rotate: 0,
                            textStyle: {
                                color: "#ffffff",
                                align: "bottom",
                            }
                        },
                        splitLine: {
                            show: false
                        },
                        data: ['1:00', '2:00', '3:00', '4:00', '5:00', '6:00']
                    }],
                    yAxis: [{ //Y轴样式
                        type: 'value',
                        // name:'233',
                        //nameLocation:'start',
                        nameGap: '0',
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            rotate: 0,
                            textStyle: {
                                color: "#ffffff",
                            }
                        },
                        splitLine: {
                            show: false,
                            lineStyle: {
                                color: '#EAEEF7',
                            }
                        },
                    }],
                    series: [{ //图表数据样式
                        type: 'line',
                        stack: '总量',
                        symbolSize: 6,
                        name: "告警",
                        smooth: true,
                        lineStyle: {
                            normal: {
                                color: '#f6f903',
                                width: 2,
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: "#f6f903",
                                borderColor: "#f6f903",
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                            offset: 0,
                                            color: 'rgba(220,153,8,1)' // 0% 处的颜色
                                        },
                                        {
                                            offset: 1,
                                            color: 'rgba(220,153,8,0)' // 100% 处的颜色
                                        }
                                    ],
                                    globalCoord: false // 缺省为 false
                                }
                            },
                        },
                        data: [100, 200, 300, 100, 200, 300]
                    }]
                }
            },
            f: function() { //利用率top5 
                return {}
            },
            g: function() { //基础资源使用量 
                let datarry = []
                // console.info('数据', this.gdata)
                if (this.gdata) {
                    //有数据时
                    this.useRatRankTypes.forEach((item) => {
                        let middleText = ''
                        let usage = (this.gdata[this.getBaseType(item.label)].usage * 100).toFixed(0) //使用率
                        let usingval = this.gdata[this.getBaseType(item.label)].using //使用值
                        let all = this.gdata[this.getBaseType(item.label)].all //总量
                        if (item.label == "CPU") {
                            // cpu是使用率
                            middleText = "CPU\n" + usage + "%"
                            usingval = usage
                        } else if (item.label == "内 存") {
                            middleText = "内存\n" + usage + "%"
                            // 转换单位 G 并精确小数
                            usingval = (usingval / 1024 / 1024 / 1024).toFixed(2)
                            all = (all / 1024 / 1024 / 1024).toFixed(2)
                        } else if (item.label == "硬 盘") {
                            middleText = "硬盘\n" + usage + "%"
                            usingval = (usingval / 1024 / 1024 / 1024).toFixed(2)
                            all = (all / 1024 / 1024 / 1024).toFixed(2)
                        }
                        datarry.push({
                            tooltip: {
                                show: false,
                                trigger: 'item',
                                formatter: "{a} <br/>{b}: {c} ({d}%)"
                            },
                            legend: {
                                orient: 'vertical',
                                x: 'center',
                                y: 'bottom',
                                top: '70%',
                                textStyle: {
                                    color: '#fff',
                                    fontSize: '14'
                                },
                                formatter: function(name, vaule) {
                                    return name
                                },
                                data: [(item.label == 'CPU' ? '使用率: ' : '使用量: ') + usingval + (item.label == 'CPU' ? '%' : 'G'), '总 量: ' + all + (item.label == 'CPU' ? '核' : 'G')]
                            },
                            graphic: {
                                type: 'text',
                                left: '39%',
                                top: '35%',
                                style: {
                                    text: middleText,
                                    fill: item.color.use,
                                    font: '1.5em "STHeiti", sans-serif'
                                }
                            },
                            series: [{
                                name: item.label,
                                type: 'pie',
                                center: ['50%', '40%'],
                                radius: ['50%', '60%'],
                                avoidLabelOverlap: false,
                                label: {
                                    normal: {
                                        show: false,
                                        position: 'center',
                                        // formatter: '{b}\n{d}',
                                        //  textStyle: {
                                        //     fontSize: '18',
                                        //     fontWeight: 'bold'
                                        // }
                                    },
                                    emphasis: {
                                        show: false,
                                        position: 'center',
                                        formatter: '{b}\n{d}%',
                                        textStyle: {
                                            fontSize: '18',
                                            fontWeight: 'bold'
                                        }
                                    }
                                },
                                labelLine: {
                                    normal: {
                                        show: false
                                    }
                                },
                                data: [{
                                        value: usingval,
                                        name: (item.label == 'CPU' ? '使用率: ' : '使用量: ') + usingval + (item.label == 'CPU' ? '%' : 'G'),
                                        itemStyle: {
                                            normal: {
                                                color: item.color.use
                                            }
                                        }
                                    },
                                    {
                                        value: (all - usingval),
                                        name: '总 量: ' + all + (item.label == 'CPU' ? '核' : 'G'),
                                        itemStyle: {
                                            normal: {
                                                color: item.color.sum
                                            }
                                        }
                                    }
                                ]
                            }]
                        })
                    })
                }
                return datarry
            },
            h: function() { //网络流入流出趋势 
                return {
                    //近一小时客流趋势chart图配置
                    title: { //图表标题
                        // text: '近一小时客流趋势',
                        // subtext: "客流量(人)",
                        textStyle: {
                            fontFamily: '微软雅黑',
                            fontWeight: 'normal', //标题颜色
                            fontSize: 17,
                            color: '#73C5FA'
                        },
                    },
                    legend: {
                        // x: 'center',
                        // y: 'bottom',
                        // top: '70%',
                        textStyle: {
                            color: '#fff',
                            fontSize: '14'
                        },
                        data: [{
                                name: '流出',
                                icon: 'roundRect'
                            },
                            {
                                name: '流入',
                                icon: 'roundRect'
                            },
                        ]
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    grid: { //图表在div的布局控制
                        top: '15%',
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [{ //X轴样式
                        type: 'category',
                        boundaryGap: false,
                        axisLine: {
                            show: false
                        },
                        axisTick: false,
                        axisLabel: {
                            rotate: 0,
                            textStyle: {
                                color: "#ffffff",
                                align: "bottom",
                            }
                        },
                        splitLine: {
                            show: false
                        },
                        data: ['1:00', '2:00', '3:00', '4:00', '5:00', '6:00']
                    }],
                    yAxis: [{ //Y轴样式
                        type: 'value',
                        // name:'233',
                        //nameLocation:'start',
                        nameGap: '0',
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            rotate: 0,
                            textStyle: {
                                color: "#ffffff",
                            }
                        },
                        splitLine: {
                            show: false,
                            lineStyle: {
                                color: '#EAEEF7',
                            }
                        },
                    }],
                    series: [{ //图表数据样式
                        type: 'line',
                        stack: '流出',
                        symbolSize: 6,
                        name: "流出",
                        smooth: true,
                        z: 2,
                        lineStyle: {
                            normal: {
                                color: '#f5fcfd',
                                width: 2,
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: "#f5fcfd",
                                borderColor: "#f5fcfd",
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                            offset: 0,
                                            color: 'rgba(3,237,255,0.4)' // 0% 处的颜色
                                        },
                                        {
                                            offset: 1,
                                            color: 'rgba(3,237,255,0)' // 100% 处的颜色
                                        }
                                    ],
                                    globalCoord: false // 缺省为 false
                                }
                            },
                        },
                        data: [100, 200, 300, 100, 200, 300]
                    }, { //图表数据样式
                        type: 'line',
                        stack: '流入',
                        symbolSize: 6,
                        name: "流入",
                        smooth: true,
                        z: 1,
                        lineStyle: {
                            normal: {
                                color: '#1107c9',
                                width: 2,
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: "#1107c9",
                                borderColor: "#1107c9",
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                            offset: 0,
                                            color: 'rgba(58,24,233,0.7)' // 0% 处的颜色
                                        },
                                        {
                                            offset: 1,
                                            color: 'rgba(58,24,233,0)' // 100% 处的颜色
                                        }
                                    ],
                                    globalCoord: false // 缺省为 false
                                }
                            },
                        },
                        data: [100, 200, 200, 400, 200, 300]
                    }]
                }
            },
            y: function() { //络流入流出top5统计
                return {}
            }
        },
        watch: {},
        methods: {
            getTopType: function(value) {
                //获取排名类型
                // console.log(value)
                switch (value) {
                    case 'CPU':
                        return 'cpu_topN'
                        break;
                    case '内 存':
                        return 'mem_topN'
                        break;
                    case '硬 盘':
                        return 'disk_topN'
                        break;
                    case '流 入':
                        return 'net_in_topN'
                        break;
                    case '流 出':
                        return 'net_out_topN'
                        break;
                    default:
                        return ''
                        break;
                }
            },
            getBaseType: function(value) {
                //获取基础数据类型
                // console.log(value)
                switch (value) {
                    case 'CPU':
                        return 'cpu'
                        break;
                    case '内 存':
                        return 'mem'
                        break;
                    case '硬 盘':
                        return 'disk'
                        break;
                    case '流 入':
                        return 'net_in'
                        break;
                    case '流 出':
                        return 'net_out'
                        break;
                    default:
                        return ''
                        break;
                }
            },
            get_overall_health: function() {
                //获取健康度
                http.get(urls.HQJKD).then(res => {
                    let data = res.data
                    this.adata = data
                    // console.log(this.adata)
                })
            },
            get_host_stat: function() {
                //获取主机信息
                http.get(urls.HQZJXX).then(res => {
                    let data = res.data
                    this.bdata = data
                    // console.log(data)
                })
            },
            get_alert_stat: function() {
                //获取告警统计信息
                http.get(urls.HQGJTJ).then(res => {
                    let data = res.data
                    this.cdata = data
                    // console.log(data)
                })
            },
            get_metric_stat: function() {
                //获取指标统计信息
                http.get(urls.HQZBTJ).then(res => {
                    let data = res.data
                    this.ddata = data
                    // console.log(data)
                })
            },
            get_out_in: function() {
                //获取网络流入流出趋势
                http.get(urls.HQJKSJ, {
                    start: '5m-ago',
                    m: 'sum:cluster.net.dev.receive'
                }).then(res => {
                    let data = res.data
                    // console.log(data)
                })
                http.get(urls.HQJKSJ, {
                    start: '5m-ago',
                    m: 'sum:cluster.net.dev.transmit'
                }).then(res => {
                    let data = res.data
                    // console.log(data)
                })
            },
            get_sys_resource: function() {
                //获取指所有Top5及基础资源使用量 
                http.get(urls.HQSYL).then(res => {
                    let data = res.data
                    let baseinfo = { //基础资源使用量
                        cpu: {
                            usage: data.cpu_usage,
                            all: data.cpu_all,
                            using: data.cpu_using,
                        },
                        mem: {
                            usage: data.mem_usage,
                            all: data.mem_all,
                            using: data.mem_using,
                        },
                        disk: {
                            usage: data.disk_usage,
                            all: data.disk_all,
                            using: data.disk_using,
                        }
                    }
                    let yjtop5 = { //硬件使用率排名
                        cpu_topN: data.cpu_topN,
                        mem_topN: data.mem_topN,
                        disk_topN: data.disk_topN,
                    }
                    let netInOutTop5 = { //网络使用率排名
                        net_in_topN: data.net_in_topN,
                        net_out_topN: data.net_out_topN,
                    }
                    let topMax = {
                        //排名最大值
                        cpu: data.cpu_topN[0],
                        mem: data.mem_topN[0],
                        disk: data.disk_topN[0],
                        net_in: data.net_in_topN[0],
                        net_out: data.net_out_topN[0],
                    }
                    this.fdata = yjtop5
                    this.gdata = baseinfo
                    this.ydata = netInOutTop5
                })
            },
            get_mycharts: function() {
                //获取自定义指标概览图表
                http.get(urls.HQZDYGLTB).then(res => {
                    let data = res.data
                    // console.log(data)
                    this.mycharts = data
                })
            },
            remove_mychart: function(chart,mychartindex) {
                //删除自定义指标概览图表
                http.post(urls.SCZDYGLTB, {
                    id: chart._id
                }).then(res => {
                    let data = res.data
                    // console.log(data)
                  
                    this.mycharts.splice(mychartindex,1)
                })

            },
            init: function() {
                this.get_overall_health()
                this.get_host_stat()
                this.get_alert_stat()
                this.get_metric_stat()
                this.get_sys_resource()
                this.get_out_in()
                this.get_mycharts()
            }
        },
        mounted() {
            //挂载时
            this.init()
        },
    }
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
    .close {
        position: absolute;
        right: 0.8rem;
    }
    .survey {}
    .survey .title {
        text-align: left;
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
        color: #41404e;
    }
    .survey .charts {
        display: flex;
        flex-wrap: wrap;
    }
    .charts .chart {
        // height: 12.35rem;
        background: rgba(12, 17, 37, 0.35);
        margin: 0.3rem 0.5%;
        border-radius: 4px;
        position: relative;
    }
    .chart .head {
        color: #fff;
        font-size: 0.9rem;
    }
    .chart .head.left {
        text-align: left;
        padding-left: 0.5rem;
        padding-top: 0.3rem;
        padding-bottom: 0.3rem;
    }
    .chart .head.center {
        text-align: center;
        padding-top: 0.3rem;
        padding-bottom: 0.3rem;
    }
    .chart25 {
        width: 24%;
    }
    .chart50 {
        width: 49%;
    }
    .chart100 {
        width: 100%;
    }
    /*总体告警*/
    .ztgj {
        padding: 2rem 0rem;
    }
    .ztgj .date {
        font-size: 1.2rem;
        color: #fff;
        float: left;
        /* margin-top: 0.4rem; */
        position: relative;
        top: 0.4rem;
        right: -1rem;
    }
    .ztgj .date .item {
        line-height: 1.6rem;
    }
    .ztgj .datename {
        font-size: 0.7rem;
        color: #fff;
        position: absolute;
        top: 5.2rem;
        right: 3.5rem;
        text-align: left;
    }
    .ztgj .datename .item {
        line-height: 1.7rem;
    }
    .ztgj .bg {
        width: 10rem;
    }
    /* 指标 */
    .chart .indicator {}
    .chart .indicator .count {
        font-size: 2.5rem;
        color: #fff;
        padding: 1.6rem 0rem;
    }
    .chart .indicator .count .unit {
        font-size: 0.9rem;
    }
    .indicator .label {
        padding: 0.2rem 0rem;
    }
    .indicator .label .name {
        font-size: 0.8rem;
        color: #fff;
    }
    .indicator .label .count {
        font-size: 0.8rem;
        color: #fff;
        display: inline-block;
        width: 2rem;
        padding: 0;
    }
    .indicator .label .processbg {
        display: inline-block;
        width: 9.6rem;
        background: #535674;
        height: 0.6rem;
        border-radius: 4px;
    }
    .indicator .label .processbg .process {
        width: 68%;
        height: 100%;
        border-radius: 4px;
    }
    /* 排名top */
    .chart .rank {}
    .chart .rank .count {
        font-size: 2.5rem;
        color: #fff;
        padding: 1.6rem 0rem;
    }
    .chart .rank .count .unit {
        font-size: 0.9rem;
    }
    .rank .label {
        padding: 0.25rem 0rem;
        margin-bottom: 0.5rem;
    }
    .rank .label .name {
        font-size: 0.8rem;
        color: #fff;
        display: inline-block;
        width: 6.2rem;
        text-align: right;
        margin-right: 0.5rem;
    }
    .rank .label .count {
        font-size: 0.8rem;
        color: #fff;
    }
    .rank .label .processbg {
        display: inline-block;
        width: 19rem;
        background: #535674;
        height: 0.6rem;
        border-radius: 4px;
    }
    .rank .label .processbg .process {
        width: 68%;
        height: 100%;
        border-radius: 4px;
    }
    /*排名tab*/
    .tabs {}
    .tabs .tab {
        font-size: 0.9rem;
        padding: 0.1rem 0rem;
        color: #657488;
        display: inline-block;
        border-bottom: 0.1rem solid;
        width: 3.4rem;
        margin: 0.2rem 0rem 1rem 0.5rem;
    }
    .userat .tabs .tab.active {
        color: #03edff;
    }
    .flow .tabs .tab.active {
        color: #ece367
    }
    .scales {
        text-align: right;
        padding-right: 1.5rem;
        font-size: 1rem;
    }
    .scales .item {
        padding: 0rem 0.5rem;
        color: #fff;
    }
</style>

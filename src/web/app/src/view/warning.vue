<template>
    <!-- 告警 -->
    <div class="warning">
        <div class="tabs">
            <div v-for="tab in tabs" :class="{'active':tabslc==tab}" @click="tabslc=tab" class="tab clickable">
                {{tab}}
            </div>
        </div>
        <div v-show="tabslc=='告警策略'" class="strategy">
            <!--策略名称-->
            <div class="generalTop">
                <div class="generalSearch">
                    <button>搜索告警项目</button>
                </div>
                <div class="searchText inputfontwhite phwhite">
                    <input class="search " v-model="searchstrategy" type="text" placeholder="请输入搜索关键字...">
                    <el-select v-model="labelsle" class="searchClass inputfontwhite phwhite" placeholder="请选择标签分类">
                        <el-option :label="'不限'" :value="'all'">
                        </el-option>
                        <el-option v-for="item in labels" :key="item.label" :label="item.label" :value="item.label">
                        </el-option>
                    </el-select>
                </div>
                <div class="searchBtn">
                    <button class='clickable' type='button' @click="searchWarn();pageactive=1;">搜索</button>
                </div>
                <div class="addView">
                    <button class='clickable' type='button' @click="editView()">新增告警策略</button>
                </div>
            </div>
            <div class="generalContent">
                <table border="0" cellspacing="0" cellpadding="0">
                    <thead>
                        <tr>
                            <td>序号</td>
                            <td>策略名称</td>
                            <td>类型</td>
                            <td>指标名</td>
                            <!-- <td>TAGS</td> -->
                            <td>通知方式</td>
                            <td>标签</td>
                            <td>状态</td>
                            <td>创建人</td>
                            <td>操作</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item,index) in strategyList">
                            <td>{{index+1}}</td>
                            <!-- 跳转指定的进程视图 -->
                            <td>{{item.property.name}}</td>
                            <td>{{item.type}}</td>
                            <td>{{item.tsd_rule.metric}}</td>
                            <!-- <td>
                                                                                                                                                                 <span class="tag" v-for="tag in item.groups">{{tag+' '}}</span> 
                                                                                                                                                            </td> -->
                            <td><span class="tag" v-for="label in item.notify.notify_method">{{label+' '}}</span></td>
                            <td>
                                <span class="tag" v-for="label in item.property.labels">{{label+' '}}</span>
                            </td>
                            <td>
                                <div v-if="item.status=='ok'" class="status on"></div>
                                <div v-if="item.status=='no'" class="status off"></div>
                                <div v-if="item.status=='alert'" class="status err"></div>
                            </td>
                            <td>{{item.property.create_user}}</td>
                            <td class="operation">
                                <a class='clickable' title="历史"><i class="icon-history"></i></a>
                                <a class='clickable' @click="editView(item,index)" title="编辑"><i class="icon-edit"></i></a>
                                <a class='clickable' @click="toggleWarn(item._id)" title="打开告警"><i class="icon-tick"></i></a>
                                <a class='clickable' @click="delWarn(item._id)" title="删除"><i class="icon-delete"></i></a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <pageIndicator :value.sync="warnpageactive" :pagecount="warnpagecount"></pageIndicator>
            <!--新增告警策略-->
            <div class="chart_box">
                <el-dialog :title="editTitle" :visible.sync="dialogVisible" size="tiny" :before-close="handleClose">
                    <div class="chart_content">
                        <div class="nav_Box">
                            <ul class="nav clearfix">
                                <li class="fl clickable" :class="{'active':warnconf.type==item.value}" @click="warnconf.type = item.value" v-for="item in warntypes">{{item.label}}</li>
                            </ul>
                            <div class="line"></div>
                        </div>
                        <div class="main_box">
                            <!-- 基本类型 -->
                            <div class="nomaltype" v-show="warnconf.type === 'basic'">
                                <div class="left_content_box">
                                    <div class="one clearfix">
                                        <p class="left_title fl">策略名称</p>
                                        <input class="text fl" placeholder="请输入..." v-model="warnconf.property.name" type="text">
                                    </div>
                                    <div class="two clearfix">
                                        <p class="left_title fl">指标名</p>
                                        <el-select @change="zbnameChange(warnconf.tsd_rule)" v-model="warnconf.tsd_rule.metric" class="fl zb_input ml" placeholder="请选择">
                                            <el-option @click="item.tag = [];" v-for="item in zbList" :key="item" :label="item" :value="item">
                                            </el-option>
                                        </el-select>
                                    </div>
                                    <div class="three clearfix">
                                        <p class="left_title fl">检查间隔</p>
                                        <input class="text fl" placeholder="请输入..." v-model="warnconf.interval" type="text">
                                    </div>
                                    <div class="three clearfix">
                                        <p class="left_title fl">TAG</p>
                                        <button class="ml fl btn clickable" @click="addgroup(warnconf.tsd_rule.group)"><i class="icon-plus"></i></button>
                                    </div>
                                    <ul>
                                        <li class="clearfix" style="margin-bottom:0.25rem;" v-for="(onegroup,index) in warnconf.tsd_rule.group">
                                            <el-select @change="tagkeychoose(warnconf.tsd_rule,onegroup)" v-model="onegroup.key" class="fl key_input" placeholder="请选择">
                                                <el-option @click="onegroup.value = '*';" v-for="item in warnconf.tsd_rule.tagkeyList" :key="item" :label="item" :value="item">
                                                </el-option>
                                            </el-select>
                                            <el-select v-model="onegroup.value" class="fl value_input ml" placeholder="请选择">
                                                <el-option :key="'*'" :label="'所有'" :value="'*'">
                                                </el-option>
                                                <el-option v-for="item in onegroup.tagvalList" :key="item" :label="item" :value="item">
                                                </el-option>
                                            </el-select>
                                            <!-- <select @change="tagkeychoose(warnconf.tsd_rule,onegroup)" v-model="onegroup.key" class="fl key_input" placeholder="请选择">
                                                                                <option v-for="item in warnconf.tsd_rule.tagkeyList" :key="item" :value="item">{{item}}</option>
                                                                            </select>
                                                                        <select v-model="onegroup.value" class="fl value_input ml" placeholder="请选择">
                                                                                    <option :key="'*'" :value="'*'">
                                                                                            所有
                                                                                    </option>
                                                                                    <option v-for="item in onegroup.tagvalList" :key="item" :value="item">{{item}}</option>
                                                                            </select> -->
                                            <button class="ml btn fl clickable" type="button" @click="delgroup(warnconf.tsd_rule.group,index)"><i class="icon-delete"></i></button>
                                        </li>
                                    </ul>
                                </div>
                                <div class="right_content_box">
                                    <div class="one clearfix">
                                        <p class="left_title fl">通知对象</p>
                                        <el-select multiple v-model="warnconf.notify.notify_user" class="fl tzdx_input ml" placeholder="请选择">
                                            <el-option v-for="item in zbList" :key="item" :label="item" :value="item">
                                            </el-option>
                                        </el-select>
                                    </div>
                                    <div class="two clearfix">
                                        <p class="left_title fl">通知方式</p>
                                        <el-checkbox-group v-model="mestypechecks">
                                            <el-checkbox v-for="(item,index) in messagetypes" :label="item.label" @change="messagetypecheck" class="tzfs_check clickable"></el-checkbox>
                                        </el-checkbox-group>
                                    </div>
                                    <div class="two clearfix">
                                        <p class="left_title fl">规则描述</p>
                                        <!-- <el-select v-model="warnconf.tsd_rule.metric" class="fl gzms_input ml" placeholder="请选择">
                                                                                                                                                            <el-option v-for="item in zbList" :key="item" :label="item" :value="item">
                                                                                                                                                            </el-option>
                                                                                                                                                        </el-select> -->
                                        <input v-model="warnconf.tsd_rule.time_duration" placeholder="请输入" class="text gzms_input fl" type="text">
                                        <el-select v-model="warnconf.tsd_rule.time_unit" class="fl gzms_input ml" placeholder="请选择">
                                            <el-option v-for="item in time_units" :key="item.label" :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                        <el-select v-model="warnconf.tsd_rule.sample" class="fl gzms_input ml" placeholder="请选择">
                                            <el-option v-for="item in samples" :key="item.label" :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                        <el-select v-model="warnconf.tsd_rule.comparison" class="fl gzms_input ml" placeholder="请选择">
                                            <el-option v-for="item in comparisons" :key="item.label" :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                        <input v-model="warnconf.tsd_rule.threshold" placeholder="阈值" class="text gzms_text fl" type="text">
                                    </div>
                                    <div class="three clearfix">
                                        <p class="left_title fl">标签</p>
                                        <button class="ml fl btn clickable" @click="addlabel(warnconf.property.labels)"><i class="icon-plus"></i></button>
                                    </div>
                                    <ul>
                                        <li class="clearfix" style="margin-bottom:0.25rem;" v-for="(label,index) in warnconf.property.labels">
                                            <input class="text fl" style="margin-left: 0" placeholder="请输入..." v-model="warnconf.property.labels[index]" type="text">
                                            <button class="ml btn fl clickable" type="button" @click="dellabel(warnconf.property.labels,index)"><i class="icon-delete"></i></button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="bottom_btnBox">
                        <button class="sureBtn clickable" v-if="editTitle=='新增告警策略'" @click="addWarn" type="button">确定</button>
                        <button class="sureBtn clickable" v-if="editTitle=='编辑告警策略'" @click="updateWarn" type="button">确定</button>
                        <button class="cancleBtn clickable" type="button" @click="dialogVisible = false">取消</button>
                    </div>
                </el-dialog>
            </div>
            <!--新增告警策略-->
        </div>
        <div v-show="tabslc=='历史记录'" class="history">
            <!-- 历史记录 -->
            <div class="generalTop">
                <div class="generalSearch">
                    <button>告警策略名称</button>
                </div>
                <div class="searchText inputfontwhite phwhite">
                    <input class="search" v-model="searchhistory" type="text" placeholder="请输入搜索关键字...">
                </div>
                <!-- 时间选择 -->
                <div class="timepicker">
                    <button>时间范围</button>
                </div>
                <div class="timeText">
                    <el-date-picker class="dateinput inputfontwhite phwhite" v-model="historydate.start" type="datetime" placeholder="请输入开始时间...">
                    </el-date-picker>
                    <!-- <input class="dateinput" v-model="historydate.start" type="text" placeholder="请输入开始时间..."> -->
                </div>
                <div class="timeline fl">—</div>
                <div class="timeText">
                    <el-date-picker class="dateinput inputfontwhite phwhite" v-model="historydate.end" type="datetime" placeholder="请输入结束时间...">
                    </el-date-picker>
                    <!-- <input class="dateinput" v-model="historydate.end" type="text" placeholder="请输入结束时间..."> -->
                </div>
                <div class="searchBtn">
                    <button class='clickable' type='button' @click="searchHistory">搜索</button>
                </div>
            </div>
            <div class="generalContent">
                <table border="0" cellspacing="0" cellpadding="0">
                    <thead>
                        <tr>
                            <td>序号</td>
                            <td>告警策略名称</td>
                            <td>时间</td>
                            <td>详细信息</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item,index) in historyList">
                            <td>{{index+1}}</td>
                            <!-- 跳转指定的进程视图 -->
                            <td>{{item.strategy_name}}</td>
                            <td>{{simdate.SJCtoTime(item.alert_time)}}</td>
                            <td>{{item.alert_info}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <pageIndicator :value.sync="historypageactive" :pagecount="historypagecount"></pageIndicator>
        </div>
    </div>
</template>
<script>
    import http from 'service/myhttp'
    import urls from 'service/url'
    import pageIndicator from 'components/pageIndicator' //分页器
    import simdate from 'service/simdate'
    export default {
        name: 'warning', //告警
        components: {
            pageIndicator
        },
        data() {
            return {
                simdate: simdate,
                warnpageactive: 1, //当前页码
                warnitemcount: 0, // 数据总数
                onepagecount: 10, //一页显示个数
                editTitle: '', //编辑视图弹窗标题
                dialogVisible: false, //编辑视图显示隐藏
                labels: [], //所有标签数组
                searchstrategy: '', //搜索策略文字
                labelsle: '', //tag选择刷选（搜索）
                editboxtype: '', //编辑框类型（新增/编辑）
                newTagName: '', //新增标签tag名
                tabslc: '告警策略', //导航选择
                tabs: [ //tabs 数组 导航数组
                    '告警策略',
                    '历史记录'
                ],
                mestypechecks: [
                    //消息选择数组
                ],
                warntypes: [ //告警类型数组
                    {
                        label: '基本类型',
                        value: 'basic'
                    }
                ],
                zbList: [ //指标名可选提示数组
                ],
                time_units: [ //时间单位数组
                    {
                        label: '秒',
                        value: 's'
                    },
                    {
                        label: '分',
                        value: 'm'
                    },
                    {
                        label: '时',
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
                        value: 'y'
                    },
                    {
                        label: '年',
                        value: 'n'
                    },
                ],
                samples: [ //取样方法数组
                    {
                        label: '平均值',
                        value: 'avg'
                    },
                    {
                        label: '最大值',
                        value: 'max'
                    },
                    {
                        label: '最小值',
                        value: 'min'
                    },
                    {
                        label: '总和',
                        value: 'sum'
                    }
                ],
                comparisons: [ //比较符数组
                    {
                        label: '大于',
                        value: '>'
                    },
                    {
                        label: '小于',
                        value: '<'
                    }, {
                        label: '等于',
                        value: '='
                    }
                ],
                // tagkeyList: [], //分组的key/value
                // tagvalList: [], //分组的key/value
                messagetypes: [{
                        label: 'API通知',
                        value: 'api'
                    },
                    {
                        label: 'slack通知',
                        value: 'slack'
                    },
                    {
                        label: '微信通知',
                        value: 'mail'
                    },
                    {
                        label: '邮件通知',
                        value: 'wechat'
                    }
                ], //通知方式数组
                warnconf: { //告警策略配置
                    property: { //基本信息
                        name: '', //策略名
                        create_user: '', //用户
                        note: '', //备注
                        labels: [ //标签数组
                        ]
                    },
                    type: 'basic', //告警类型
                    tsd_rule: { //规则
                        metric: '', //指标名
                        time_duration: 0, //时间长度
                        time_unit: '', //时间单位
                        sample: '', //取样方法
                        comparison: '', //比较符
                        threshold: '', //阈值
                        tagkeyList: [],
                        group: [{
                            key: '',
                            value: '',
                            tagvalList: []
                        }], //分组（TAGS）
                        interval: 0, //检查间隔
                        status: 'on', //状态（on/off/alert）
                        level: '', //重要程度
                    },
                    interval: 0, //检查间隔
                    notify: { // 通知
                        notify_method: [], //通知方式（列表）
                        notify_user: [], //通知用户（列表）
                        // notify_group:[] //通知用户组
                    }
                },
                strategyList: [ //表格列表数据数组
                    {
                        property: { //基本信息
                            name: '', //策略名
                            create_user: '', //用户
                            note: '', //备注
                            labels: [ //标签数组
                            ]
                        },
                        type: 'basic', //告警类型
                        tsd_rule: { //规则
                            metric: '', //指标名
                            time_duration: 0, //时间长度
                            time_unit: '', //时间单位
                            sample: '', //取样方法
                            comparison: '', //比较符
                            threshold: '', //阈值
                            tagkeyList: [],
                            group: [{
                                key: '',
                                value: '',
                                tagvalList: []
                            }], //分组（TAGS）
                            interval: 0, //检查间隔
                            status: 'on', //状态（on/off/alert）
                            level: '', //重要程度
                        },
                        notify: { // 通知
                            notify_method: [], //通知方式（列表）
                            notify_user: [], //通知用户（列表）
                            // notify_group:[] //通知用户组
                        }
                    }
                ],
                /*--历史记录的状态机--*/
                historypageactive: 1, //当前页码
                historyitemcount: 0, // 数据总数
                searchhistory: '', //搜索历史（文字）
                historydate: {
                    start: '', //开始时间
                    end: '' //结束时间
                },
                historyList: [ //历史记录数组
                    {
                        name: 'rdjrdj', //策略名称
                        date: '', //时间
                        info: '', //详细信息
                    }
                ]
            }
        },
        computed: {
            warnpagecount: function() {
                //告警页面总数 （每页10个）
                return parseInt(this.warnitemcount / this.onepagecount) + (parseInt(this.warnitemcount % this.onepagecount) > 0 ? 1 : 0)
            },
            historypagecount: function() {
                //告警页面总数 （每页10个）
                return parseInt(this.historyitemcount / this.onepagecount) + (parseInt(this.historyitemcount % this.onepagecount) > 0 ? 1 : 0)
            },
            hisdateval: function() {
                //告警历史日期
                let date = {
                    start: simdate.TimetoSJC(this.historydate.start),
                    end: simdate.TimetoSJC(this.historydate.end)
                }
                // console.info('告警历史', this.historydate.start)
                return date
            }
        },
        watch: {
            warnpageactive: function(val) {
                //页号发生变化
                this.initWarnInfo()
            },
            historypageactive: function(val) {
                //页号发生变化
                this.initHistoryInfo()
            },
            warnconf: function name(val) {
                //监听配置变化是否选择编辑其他项
                // console.info('配置变化', val)
                let arry = []
                this.warnconf.notify.notify_method.forEach((item) => {
                    arry.push(this.getmestypelabel(item))
                })
                this.mestypechecks = arry
            }
        },
        methods: {
            gettagkey: function(item) {
                //获取tag key
                return new Promise((resolve, reject) => {
                    http.get(urls.LQTAGKEY, { //拉取TAG的key
                        period: '10m-ago', //时间范围
                        metric: 'sum:' + item.metric,
                    }).then(
                        res => {
                            let data = res.data.data
                            item.tagkeyList = data[0].aggregateTags
                            resolve(res)
                        }, err => {
                            reject(err)
                        })
                })
            },
            gettagvalue: function(item, tag) {
                //获取tag value
                return new Promise((resolve, reject) => {
                    http.get(urls.LQTAGVAL, { //拉取TAG的key/value
                        start: '10m-ago', //时间范围
                        m: 'sum:' + item.metric + '{' + tag.key + '=*}',
                        // max: 99999
                    }).then(res => {
                        tag.tagvalList = [] //数据库不可能记录这个列表所以要初始化
                        let data = res.data
                        data.forEach(onedata => {
                            //遍历数据 （数据库接口奇葩）
                            // console.info('tag数据', onedata)
                            tag.tagvalList.push(onedata.tags[tag.key])
                        })
                        resolve(data)
                    }, err => {
                        reject(err)
                    })
                })
            },
            zbnameChange: function(item) {
                //指标名更改
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
            editView: function(item) {
                //新增，编辑告警策略
                if (item) {
                    //编辑告警策略
                    // console.info('编辑配置',item)
                    this.editTitle = '编辑告警策略'
                    // this.warnconf.name = item.name
                    // this.warnconf.type = item.type
                    // this.warnconf.tsd_rule.metric = item.metric
                    // this.warnconf.tsd_rule.group = item.groups
                    // this.warnconf.labels = item.labels
                    let gettagvalues = [] //获取标签值请求数组
                    if (item.tsd_rule.metric != null && item.tsd_rule.metric != '') {
                        gettagvalues.push(this.gettagkey(item.tsd_rule))
                        item.tsd_rule.group.forEach((onetag) => {
                            if (onetag.key != null && onetag.key != '') {
                                // console.info('其中一个tag', onetag)
                                gettagvalues.push(this.gettagvalue(item.tsd_rule, onetag))
                            }
                        })
                        Promise.all(gettagvalues).then(datas => {
                            this.warnconf = item
                            
                        })
                    }
                } else {
                    //新增告警策略
                    this.editTitle = '新增告警策略'
                    this.warnconf = { //告警策略配置
                        property: { //基本信息
                            name: '', //策略名
                            create_user: '', //用户
                            note: '', //备注
                            labels: [ //标签数组
                            ]
                        },
                        type: 'basic', //告警类型
                        tsd_rule: { //规则
                            metric: '', //指标名
                            time_duration: 0, //时间长度
                            time_unit: '', //时间单位
                            sample: '', //取样方法
                            comparison: '', //比较符
                            threshold: '', //阈值
                            tagkeyList: [], //标签键值数组
                            group: [{
                                key: '',
                                value: '',
                                tagvalList: []
                            }], //分组（TAGS）
                            interval: 0, //检查间隔
                            status: 'on', //状态（on/off/alert）
                            level: '', //重要程度
                        },
                        interval: 0,
                        notify: { // 通知
                            notify_method: [], //通知方式（列表）
                            notify_user: [] //通知用户（列表）
                        }
                    }
                }
                this.dialogVisible = true;
            },
            handleClose: function() {
                this.dialogVisible = false;
            },
            getmestypeval: function(value) {
                //获取通知方式值
                let data
                switch (value) {
                    case 'API通知':
                        data = 'api'
                        break;
                    case 'slack通知':
                        data = 'slack'
                        break;
                    case '微信通知':
                        data = 'wechat'
                        break;
                    case '邮件通知':
                        data = 'mail'
                        break;
                    default:
                        data = ''
                        break;
                }
                return data
            },
            getmestypelabel: function(value) {
                //获取通知方式显示文字
                let data
                switch (value) {
                    case 'api':
                        data = 'API通知'
                        break;
                    case 'slack':
                        data = 'slack通知'
                        break;
                    case 'wechat':
                        data = '微信通知'
                        break;
                    case 'mail':
                        data = '邮件通知'
                        break;
                    default:
                        data = ''
                        break;
                }
                return data
            },
            messagetypecheck: function(even) {
                //通知方式多选
                let value //真正值
                let check = even.target.checked
                value = this.getmestypeval(even.target.value)
                if (check == true) {
                    this.warnconf.notify.notify_method.push(value)
                } else {
                    this.warnconf.notify.notify_method.forEach((item, index) => {
                        if (item == value) {
                            this.warnconf.notify.notify_method.splice(index)
                        }
                    });
                }
                // console.log(even)
            },
            getlabels: function() {
                //获取标签数组
                http.get(urls.HQGJBQSZ).then(res => {
                    let data = res.data
                    this.labels = data
                })
            },
            getWarnCount: function() {
                // 获取告警策略数据总数
                // console.log(this)
                http.get(urls.HQCLZS, {
                    text: this.searchstrategy,
                    label: this.labelsle
                }).then(res => {
                    // console.log(res)
                    let data = res.data
                    this.warnitemcount = data.count
                })
            },
            getHistoryCount: function() {
                //获取告警历史数据总数
                // console.log(this)
                http.get(urls.HQLSZS, {
                    text: this.searchhistory,
                    date: this.hisdateval
                }).then(res => {
                    // console.log(res)
                    let data = res.data
                    this.historyitemcount = data.count
                })
            },
            searchWarn: function() {
                //搜索告警策略
                // console.log(this)
                http.get(urls.HQGJCL, {
                    text: this.searchstrategy, //刷选文本
                    label: this.labelsle, //标签选择
                    page: this.warnpageactive, //页号
                    onepagecount: this.onepagecount //每页数量
                }).then(res => {
                    // console.log(res)
                    let data = res.data
                    // console.log(data)
                    this.strategyList = data
                })
            },
            searchHistory: function() {
                //搜索告警历史
                // console.log(this)
                http.get(urls.HQGJLS, {
                    text: this.searchhistory, //刷选文本
                    page: this.historypageactive, //页号
                    onepagecount: this.onepagecount, //每页数量
                    date: this.hisdateval, //日期
                }).then(res => {
                    // console.log(res)
                    let data = res.data
                    // console.log(data)
                    this.historyList = data
                })
            },
            addWarn: function() {
                // 添加告警策略
                // console.log(this)
                let newoption = Object.assign({}, this.warnconf) //新图表数据 （对象深拷贝）（发送前处理掉数据库不要的数据） 
                delete(newoption.tsd_rule.tagkeyList)
                newoption.tsd_rule.group.forEach(tag => {
                    delete(tag.tagvalList)
                })
                http.post(urls.TJGJCL, {
                    option: newoption,
                }).then(res => {
                    // console.log(res)
                    this.initWarnInfo()
                    this.handleClose()
                    this.$message({
                        showClose: true,
                        message: '操作成功',
                        type: 'success'
                    })
                })
            },
            updateWarn: function() {
                //更新告警策略
                // console.log(this)
                let newoption = Object.assign({}, this.warnconf) //新图表数据 （对象深拷贝）（发送前处理掉数据库不要的数据） 
                delete(newoption.tsd_rule.tagkeyList)
                newoption.tsd_rule.group.forEach(tag => {
                    delete(tag.tagvalList)
                })
                http.post(urls.GXGJCL, {
                    option: newoption,
                }).then(res => {
                    // console.log(res)
                    this.initWarnInfo()
                    this.handleClose()
                    this.$message({
                        showClose: true,
                        message: '操作成功',
                        type: 'success'
                    })
                })
            },
            delWarn: function(id) {
                // 删除告警策略
                // console.log(this)
                // let id=this.warnconf._id
                http.post(urls.SCGJCL, {
                    id: id,
                }).then(res => {
                    // console.log(res)
                    this.initWarnInfo()
                    this.$message({
                        showClose: true,
                        message: '操作成功',
                        type: 'success'
                    })
                })
            },
            toggleWarn: function(id) {
                // 切换告警开关
                // console.log(this)
                http.post(urls.QHGJKG, {
                    id:id  
                }).then(res => {
                    // console.log(res)
                 this.$message({
                        showClose: true,
                        message: '操作成功',
                        type: 'success'
                    })
                })
            },
            addgroup: function(groups) {
                //批量添加tag
                groups.push({ //分组
                    key: '', //键值
                    value: '' //值
                })
            },
            delgroup: function(groups, index) {
                //删除分组
                groups.splice(index, 1)
            },
            addlabel: function(labels) {
                //批量添加标签
                labels.push('')
            },
            dellabel: function(labels, index) {
                //删除标签
                labels.splice(index, 1)
            },
            initWarnInfo: function() {
                //初始化告警数据
                this.getlabels()
                this.getWarnCount()
                this.searchWarn()
            },
            initHistoryInfo: function() {
                //初始化告历史数据
                this.getHistoryCount()
                this.searchHistory()
            }
        },
        mounted() {
            //挂载时
            http.get(urls.LQZBMLB, { //拉取指标名列表
                type: 'metrics'
            }).then(res => {
                let data = res.data
                this.zbList = data
                // console.log(data)
            })
            this.initWarnInfo()
            this.initHistoryInfo()
        },
    }
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
    .warning {}
    /*--告警tabs 切换导航--*/
    .warning .tabs {
        width: 100%;
        border-bottom: 0.1rem solid #679AB5;
        margin-bottom: 0.6rem;
        color: #679AB5;
        text-align: left;
    }
    .warning .tabs .tab {
        position: relative;
        bottom: -0.1rem;
        margin-right: 1.8rem;
        display: inline-block;
        padding: 0.6rem 0.15rem;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .warning .tabs .tab.active {
        color: #fff;
        border-bottom: 0.15rem solid #fff;
    }
    /*---*/
    .search input::-webkit-input-placeholder,
    .searchClass input::-webkit-input-placeholder,
    {
        color: #c9e7ee;
        font-size: 0.9rem;
    }
    .generalSearch {
        float: left;
    }
    .generalSearch button {
        background: rgba(68, 67, 80, 0.6);
        width: 5rem;
        height: 1.5rem;
        border-radius: 0.3rem;
        line-height: 1.5rem;
        border-width: 0;
        font-size: 0.7rem;
        color: #fff;
        outline: none;
    }
    .strategy .searchText {
        float: left;
        width: 21.2rem;
        margin-left: 0.5rem;
        border-radius: 0.3rem;
        background: rgba(75, 77, 82, 0.31);
        height: 1.5rem;
        line-height: 1.1rem;
        padding: 0.2rem 0;
        box-sizing: border-box;
    }
    .strategy .searchText input {
        background: transparent;
        box-sizing: border-box;
        border-width: 0;
        outline: none;
        padding: 0 0.5rem;
        float: left;
        height: 100%;
        font-size: 0.7rem;
    }
    .strategy .searchText .search {
        width: 13.35rem;
        margin-left: -1px;
        border-right: 1px solid #84c7e2 !important;
    }
    .searchClass {
        width: 7.8rem
    }
    .searchBtn {
        float: left;
    }
    .searchBtn button {
        margin-left: 0.5rem;
        background: #57a0e8;
        width: 3.5rem;
        height: 1.5rem;
        border-radius: 0.3rem;
        line-height: 1.5rem;
        border-width: 0;
        font-size: 0.7rem;
        color: #fff;
        outline: none;
    }
    .addView {
        float: right;
    }
    .addView button {
        background: #53c1b9;
        width: 6rem;
        height: 1.5rem;
        border-radius: 0.3rem;
        line-height: 1.5rem;
        border-width: 0;
        font-size: 0.7rem;
        color: #fff;
        outline: none;
    }
    .generalContent {
        width: 61.5rem;
        height: 19.35rem;
        background: rgba(12, 17, 37, 0.25);
        clear: both;
        border-radius: 0.3rem;
        padding: 0 1rem 1rem 1rem;
        box-sizing: border-box;
    }
    .generalContent table {
        width: 100%;
    }
    .generalContent table .index {
        text-align: left;
    }
    .generalContent table input[type="checkbox"] {
        vertical-align: middle;
        width: 0.8rem;
        height: 0.8rem;
        margin-right: 0.8rem;
    }
    .generalContent table .operation a {
        display: inline-block;
        height: 100%;
        margin-right: 0.1rem;
    }
    .generalContent table .operation i {
        color: #66a5ef;
    }
    .generalContent table .operation a:nth-child(1) {
        text-align: right;
    }
    .generalContent table .operation a:nth-child(2) {
        text-align: left;
    }
    .viewname {
        color: RGB(102, 168, 239) !important;
    }
    .icon-prepared {
        margin-right: 0.15rem;
    }
    .icon-delete {
        margin-left: 0.15rem;
    }
    .generalTop {
        margin-bottom: 0.5rem;
        overflow: hidden;
    }
    .generalContent table thead td {
        height: 1.7rem;
        line-height: 1.5rem;
        font-size: 0.75rem;
        color: #fff;
        padding: 0rem 0.5rem;
    }
    .generalContent table tbody td {
        height: 1.7rem;
        line-height: 1.5rem;
        font-size: 0.65rem; // font-weight: lighter;
        color: #fff;
        padding: 0rem 0.5rem;
    }
    .generalContent table tbody tr:nth-child(odd) {
        background: #526f8a;
    }
    .generalContent table tbody tr:nth-child(odd) td {
        border-top: 1px solid #3d556c;
        border-bottom: 1px solid #3d556c;
    }
    /*视图组件*/
    .addViewMask,
    .editViewMask {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: 1000000;
    }
    .editView {
        background: #000;
        width: 27rem;
        padding: 0 2.5rem;
        height: 16.75rem;
        border-radius: 0.3rem;
        margin: 0 auto;
        position: relative;
        box-sizing: border-box;
        top: 50%;
        transform: translateY(-50%);
    }
    .MaskBtn {
        width: 5.8rem;
        height: 2rem;
        border-radius: 0.3rem;
        line-height: 2rem;
        border-width: 0;
        font-size: 0.45rem;
        color: #fff;
        outline: none;
        margin-top: 2.5rem;
    }
    .editViewOk {
        margin-right: 0.95rem;
        border: 1px solid #000;
        background: #57a0e8;
    }
    .editViewcancel {
        margin-left: 0.95rem;
        border: 1px solid #57a0e8;
        background: transparent;
    }
    .viewTitle {
        font-size: 1rem;
        color: #fff;
        padding: 1.6rem 0;
        text-align: center;
    }
    .viewNameText {
        width: 16.35rem;
        margin-left: 0.5rem;
        display: inline-block;
        line-height: 1.7rem;
        outline: none;
        color: #0da2c3;
        float: left;
        background: rgb(31, 38, 51);
        border: 0;
        font-size: 0.8rem;
        padding-left: 0.5rem;
        box-sizing: border-box;
    }
    .addViewText,
    .addViewLabeled span {
        display: inline-block;
        float: left;
        margin-left: 0.25rem;
        background: rgb(31, 38, 51);
        line-height: 1.7rem;
        width: 1.8rem;
    }
    .editViewMask .viewName {
        width: 5.4rem;
        display: inline-block;
        line-height: 1.7rem;
        text-align: center;
        color: #0da2c3;
        font-size: 0.8rem;
        float: left;
        background: rgb(31, 38, 51);
    }
    .editViewMask span {
        display: inline-block;
        height: 1.7rem;
    }
    .viewNameMask {
        text-align: left;
        overflow: hidden;
    }
    .addViewLabel,
    .addViewLabeled {
        margin-top: 0.25rem;
        overflow: hidden;
    }
    .addViewLabeled {
        margin-left: 5.65rem;
        text-align: left;
    }
    .addViewLabeled span {
        text-align: center;
    }
    .addViewLabeled span i {
        font-size: 0.8rem;
    }
    .addViewLabeled input {
        width: 14.25rem;
        line-height: 1.7rem;
        color: #0da2c3;
        font-size: 0.8rem;
        border-width: 0;
        outline: none;
        float: left;
        padding-left: 0.5rem;
        box-sizing: border-box;
        background: rgb(31, 38, 51);
    }
    .addViewLabeled .icon-delete {
        height: 1.7rem;
        line-height: 1.7rem;
        margin: 0;
        color: #fff;
    }
    .warning .status {
        width: 2.4rem;
        height: 0.5rem;
        margin: auto;
    }
    .status.on {
        background-color: #81C16A
    }
    .status.off {
        background-color: #BFBFBF
    }
    .status.err {
        background-color: #EB6876
    }
    /*--历史记录样式--*/
    .history .searchText {
        float: left;
        width: 13.35rem;
        margin-left: 0.5rem;
        border-radius: 0.3rem;
        background: rgba(75, 77, 82, 0.31);
        height: 1.5rem;
        line-height: 1.1rem;
        padding: 0.2rem 0;
        box-sizing: border-box;
    }
    .history .searchText input {
        background: transparent;
        box-sizing: border-box;
        border-width: 0;
        outline: none;
        padding: 0 0.5rem;
        float: left;
        height: 100%;
        font-size: 0.7rem;
    }
    .history .searchText .search {
        width: 13.35rem;
        margin-left: -1px;
    }
    .timepicker {
        float: left;
    }
    .history .timeText {
        float: left;
        width: 13.35rem;
        border-radius: 0.3rem;
        background: rgba(75, 77, 82, 0.31);
        height: 1.5rem;
        line-height: 1.1rem;
        padding: 0.2rem 0;
        box-sizing: border-box;
    }
    .history .timeText input {
        background: transparent;
        box-sizing: border-box;
        border-width: 0;
        outline: none;
        padding: 0.5rem;
        float: left;
        height: 100%;
        font-size: 0.7rem;
    }
    .history .timeText .dateinput {
        width: 13.35rem;
        height: 100%;
        margin-left: -1px;
    }
    .history .timeline {
        line-height: 1.5rem;
        padding: 0rem 0.3rem;
    }
    .history .timepicker button {
        background: rgba(68, 67, 80, 0.6);
        width: 5rem;
        height: 1.5rem;
        border-radius: 0.3rem;
        line-height: 1.5rem;
        border-width: 0;
        font-size: 0.7rem;
        color: #fff;
        outline: none;
        margin-left: 0.5rem;
        margin-right: 0.5rem;
    }
</style>

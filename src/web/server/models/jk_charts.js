//监控图表配置模型
let mongoose = require('mongoose');
let connections = require('../db_connect')
let Schema = mongoose.Schema;

let jk_datatime_configs = new Schema({ //监控视图时间配置
    viewid: { type: Schema.Types.ObjectId, ref: 'jk_viewlists' }, //视图id
    start: Date, //开始时间
    end: Date, //结束时间
    datetext: String, //时间文字描述
    reloadhz: Number //刷新频率
})

let jk_chart_nomals = new Schema({ //监控图表基础信息
    viewid: { type: Schema.Types.ObjectId, ref: 'jk_viewlists' }, //视图id
    title: { type: String, default: '未知图表' }, //图表标题
    type: String, //图表类型 
    xnzbs: [{ type: Schema.Types.ObjectId, ref: 'jk_chart_xnzbs' }], //相关性能指标
    yconfig: { type: Schema.Types.ObjectId, ref: 'jk_chart_ytypes' } //相关y轴配置
});
let jk_chart_xnzbs = new Schema({ //监控图表性能指标
    chartid: { type: Schema.Types.ObjectId, ref: 'jk_chart_nomals' },
    zbname: String, //指标名称
    xlname: String, //序列名称
    qytime: String, //取样时间
    qytimed: String, //取样时间单位
    aggfun: String, //聚合函数
    qyfun: String, //取样函数
    yselect: String, //y轴选择 （左或右）
    tag: [{ //标签
        key: String, //键值
        value: String //值
    }],
});


let yconfig = new Schema({ //监控图表y轴设置

    //右边y轴
    type: String, //类型
    unit: String //单位

});

let jk_chart_ytypes = new Schema({ //监控图表y轴设置
    chartid: { type: Schema.Types.ObjectId, ref: 'jk_chart_nomals' },
    left: {
        type: yconfig,
        required: true
    },
    right: {
        type: yconfig,
        required: true
    }
});

module.exports = {
        // jk_chart_nomals: connections.test.model('jk_chart_nomals', jk_chart_nomals), //监控图表基础信息
        // jk_chart_xnzbs: connections.test.model('jk_chart_xnzbs', jk_chart_xnzbs), //监控图表性能指标
        // jk_chart_ytypes: connections.test.model('jk_chart_ytypes', jk_chart_ytypes), //监控图表y轴设置
        jk_datatime_configs: connections.argus.model('jk_datatime_configs', jk_datatime_configs), //监控数据显示时间范围配置
        jk_chart_nomals: connections.argus.model('jk_chart_nomals', jk_chart_nomals), //监控图表基础信息
        jk_chart_xnzbs: connections.argus.model('jk_chart_xnzbs', jk_chart_xnzbs), //监控图表性能指标
        jk_chart_ytypes: connections.argus.model('jk_chart_ytypes', jk_chart_ytypes), //监控图表y轴设置
    } //监控图表配置模型
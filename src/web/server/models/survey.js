//总体概况
let mongoose = require('mongoose');
let connections = require('../db_connect')
let Schema = mongoose.Schema;

let overall_health = new Schema({ // 健康度
    check_time: Number, //时间戳
    score: Number //评分
});

let host_stat = new Schema({ // 主机
    check_time: Number, //时间戳
    hosts: Number, //总数
    hosts_normal: Number, //正常
    hosts_error: Number, //异常
    hosts_closed: Number //关闭
});

let alert_stat = new Schema({ // 告警统计
    check_time: Number, //时间戳
    alerts: Number, //现有告警数
    warn_alerts: Number, //告警产生数
    critical_alerts: Number //告警撤销数
});

let metric_stat = new Schema({ // 指标统计
    check_time: Number, //时间戳
    metrics: Number, //总数
    normal: Number, //正常 
    error: Number //异常
});

// 告警趋势 -> 待定

let ranking_data = new Schema({ //资源使用排名数据样式
    host: String, //主机名
    usage: Number //用量
})

let sys_resource = new Schema({ // 所有Top5及基础资源使用量 
    check_time: Number, //时间戳
    cpu_usage: Number, //cpu使用率
    cpu_all: Number, //cpu总量
    cpu_using: Number, //cpu使用量
    mem_usage: Number, //内存使用率
    mem_all: Number, //内存总量
    mem_using: Number, //内存使用量
    disk_usage: Number, //硬盘使用率
    disk_all: Number, //硬盘总量
    disk_using: Number, //硬盘使用量
    cpu_topN: [{
        host: String, //主机名
        usage: Number //用量
    }], //cpu排名
    mem_topN: [{
        host: String, //主机名
        usage: Number //用量
    }], //内存排名
    disk_topN: [{
        host: String, //主机名
        usage: Number //用量
    }], //硬盘排名
    net_in_topN: [{
        host: String, //主机名
        usage: Number //用量
    }], //网络流入排名
    net_out_topN: [{
            host: String, //主机名
            usage: Number //用量
        }] //网络流出排名
});

//网络流入/流出趋势, 大数据指标概览 -> OpenTSDB.api

let overview_indexs = new Schema({ //大数据指标概览 （就是放在概览页面的视图图表）
    chart: { type: Schema.Types.ObjectId, ref: 'jk_chart_nomals' } //视图图表id
})

/* model第三个参数是自定义集合名 否则生成集合有s */

module.exports = {
    overall_health: connections.argus_statistics.model('overall_health', overall_health, 'overall_health'), //健康度
    host_stat: connections.argus_statistics.model('host_stat', host_stat, 'host_stat'), //主机信息
    alert_stat: connections.argus_statistics.model('alert_stat', alert_stat, 'alert_stat'), //告警统计信息
    metric_stat: connections.argus_statistics.model('metric_stat', metric_stat, 'metric_stat'), //指标统计信息
    sys_resource: connections.argus_statistics.model('sys_resource', host_stat, 'sys_resource'), //所有Top5及基础资源使用量 
    overview_indexs: connections.argus.model('overview_indexs', overview_indexs) //大数据指标概览
}
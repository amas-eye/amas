//告警
let mongoose = require('mongoose');
let connections = require('../db_connect')
let Schema = mongoose.Schema;

let labels = new Schema({ //告警label标签列表
    label: String, //标签
});

let property = new Schema({ //基础信息
    name: String, //告警策略名
    create_user: String, //创建用户
    create_time: { type: Date, default: Date.now }, //创建时间(时间戳)
    update_time: { type: Date, default: Date.now }, //更改时间(时间戳)
    note: String, //备注
    labels: [{ type: String }] //标签数组
});

let tsd_rule = new Schema({ // 规则
    metric: String, //指标名
    time_duration: Number, //时间长度
    time_unit: String, //时间单位
    sample: String, //取样方法
    comparison: String, //比较符
    threshold: String, //阈值
    group: [{ //分组（TAGS）
        key: String, //键值
        value: String //值
    }]
});

let notify = new Schema({ // 通知
    notify_method: Array, //通知方式（列表）
    notify_user: String //通知用户（列表）
        // notify_group: Arry//通知用户组
});

let strategy = new Schema({ // 告警策略
    property: { type: property }, //基础信息
    type: String, //告警类型
    tsd_rule: { type: tsd_rule }, // 规则
    interval: Number, //检查间隔
    status: { type: String, default: 'no' }, //状态（on/off/alert）
    level: String, //重要程度
    notify: { type: notify } // 通知
});

let alert_history = new Schema({ // 历史记录
    strategy_name: String, //策略名
    alert_time: Number, //告警时间戳
    alert_info: String //告警内容（前端需支持换行符"\n"显示）
});


/* model第三个参数是自定义集合名 否则生成集合有s */

module.exports = {

    labels: connections.argus_alert.model('alert_labels', labels, 'alert_labels'), //告警策略标签label
    strategy: connections.argus_alert.model('strategy', strategy, 'strategy'), //告警策略
    history: connections.argus_alert.model('alert_history', alert_history, 'alert_history'), //历史记录

}
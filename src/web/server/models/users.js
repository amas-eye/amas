//用户表模型
let mongoose = require('mongoose');
let connections = require('../db_connect')
let Schema = mongoose.Schema;

let users = new Schema({ //监控项目用户信息表
    username: String, //用户名
    password: String, //密码
    create_time: { type: Date, default: Date.now }, //创建时间
    update_time: { type: Date, default: Date.now }, //更新时间
    is_admin: Boolean, //是否管理员
    group_name: [{ type: String, ref: 'groups' }], //分组名(联表分组)
    mail: String, //邮件
    cell_phone: String, //手机
    wechat_id: String, //微信
    slack_hook: String //Slack
});

// module.exports = connections.test.model('users', users) //用户模型
module.exports = connections.argus.model('users', users) //用户模型
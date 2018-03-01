//用户分组表模型
let mongoose = require('mongoose');
let connections = require('../db_connect')
let Schema = mongoose.Schema;

let groups = new Schema({ //监控项目用户分组
    group_name: String, //分组名
    users: [{ type: Schema.Types.ObjectId, ref: 'users' }] //用户id
});

// module.exports = connections.test.model('groups', groups) //用户分组操作模型
module.exports = connections.argus.model('groups', groups) //用户分组操作模型
//监控视图列表模型
let mongoose = require('mongoose');
let connections = require('../db_connect')
let Schema = mongoose.Schema;

let jk_viewlists = new Schema({ //监控视图列表
    name: String, //视图名称
    tags: [{ type: String, ref: 'jk_tags' }], //标签数组
    creater: String, //创建者
    create_time: { type: Date, default: Date.now }, //创建时间
});


// module.exports = connections.test.model('jk_viewlists', jk_viewlists) //监控视图列表
module.exports = connections.argus.model('jk_viewlists', jk_viewlists) //监控视图列表
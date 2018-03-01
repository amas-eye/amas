//监控标签tag
let mongoose = require('mongoose');
let connections = require('../db_connect')
let Schema = mongoose.Schema;

let jk_tags = new Schema({ //监控视图tag列表
    tag: String, //标签
    // viewids:[{type:Schema.Types.ObjectId,ref:'jk_viewlists'}] //视图id 数组
});

// module.exports = connections.test.model('jk_tags', jk_tags) //监控视图列表

module.exports = connections.argus.model('jk_tags', jk_tags) //监控视图列表
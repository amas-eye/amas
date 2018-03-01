/**
 * Created by Administrator on 2017/4/13.
 * mongodb 数据库的连接们
 */

// let HOST = '10.17.35.43' //内网数据库地址
// let HOST = '183.3.139.134' //外网数据库地址
let HOST = '192.168.0.253' //公司本部内网
    // let HOST = 'localhost' //本地数据库地址

let mongoose = require('mongoose');
mongoose.Promise = global.Promise; //原生es6 promise

let connect_Test = () => {
    //Test数据库链接
    let dbConnection = mongoose.createConnection(
        'mongodb://localhost/test', {
            config: {
                autoIndex: false //不自动创建索引
            },
            server: {
                auto_reconnect: true //自动重连
            }
        }
    );
    //console.log(dbConnection)

    dbConnection.on('open', () => {
        console.log('Test连接数据成功')
    })

    dbConnection.on('error', function(error) {
        console.error('Error in MongoDb connection: ' + error);
        dbConnection.disconnect();
    });

    dbConnection.on('close', function() {
        console.log('数据库断开');
    });

    return dbConnection;
}

let connect_argus = () => {
    //argus_web数据库链接
    let dbConnection = mongoose.createConnection(
        'mongodb://' + HOST + '/argus-web', {
            config: {
                autoIndex: false //不自动创建索引
            },
            server: {
                auto_reconnect: true //自动重连
            }
        }
    );
    //console.log(dbConnection)

    dbConnection.on('open', () => {
        console.log('argus-web连接数据成功')
    })

    dbConnection.on('error', function(error) {
        console.error('Error in MongoDb connection: ' + error);
        dbConnection.disconnect();
    });

    dbConnection.on('close', function() {
        console.log('argus-web数据库断开');
    });

    return dbConnection;
}

let connect_argus_statistics = () => {
    //argus_statistics数据库链接
    let dbConnection = mongoose.createConnection(
        'mongodb://' + HOST + '/argus-statistics', {
            config: {
                autoIndex: false //不自动创建索引
            },
            server: {
                auto_reconnect: true //自动重连
            }
        }
    );
    //console.log(dbConnection)

    dbConnection.on('open', () => {
        console.log('argus-statistics连接数据成功')
    })

    dbConnection.on('error', function(error) {
        console.error('Error in MongoDb connection: ' + error);
        dbConnection.disconnect();
    });

    dbConnection.on('close', function() {
        console.log('argus-statistics数据库断开');
    });

    return dbConnection;
}

let connect_argus_alert = () => {
    //argus_alert数据库链接
    let dbConnection = mongoose.createConnection(
        'mongodb://' + HOST + '/argus-alert', {
            config: {
                autoIndex: false //不自动创建索引
            },
            server: {
                auto_reconnect: true //自动重连
            }
        }
    );
    //console.log(dbConnection)

    dbConnection.on('open', () => {
        console.log('argus_alert连接数据成功')
    })

    dbConnection.on('error', function(error) {
        console.error('Error in MongoDb connection: ' + error);
        dbConnection.disconnect();
    });

    dbConnection.on('close', function() {
        console.log('argus-statistics数据库断开');
    });

    return dbConnection;
}
module.exports = {
    // test: connect_Test(), // test数据库的链接
    argus: connect_argus(), //argus-web数据库 监控
    argus_statistics: connect_argus_statistics(), //argus-statistics数据库 总体概况
    argus_alert: connect_argus_alert() //argus-alert数据库 告警
}
#!/usr/bin/env node

/**
 * Module dependencies.
 */

let app = require('../app'); //网站根目录即路由
let debug = require('debug')('node_test:server'); //调试输出模块
let http = require('http');

/**
 * Get port from environment and store in Express.
 */

// let myport = '6002' //本地
let myport = '8080' //部署
let port = normalizePort(process.env.PORT || myport); //网站端口
app.set('port', port);

/**
 * Create HTTP server.
 */

let server = http.createServer(app); //http服务api创建http服务器

/**
 * Listen on provided port, on all network interfaces.
 */

server.listen(port);
server.on('error', onError);
server.on('listening', onListening);

/**
 * Normalize a port into a number, string, or false.
 */

function normalizePort(val) { //根据判断生成端口
    let port = parseInt(val, 10);

    if (isNaN(port)) {
        // named pipe
        return val;
    }

    if (port >= 0) {
        // port number
        return port;
    }

    return false;
}

/**
 * Event listener for HTTP server "error" event.
 */

function onError(error) { //监听http服务启动错误并判断错误类型打印信息
    if (error.syscall !== 'listen') {
        throw error;
    }

    let bind = typeof port === 'string' ?
        'Pipe ' + port :
        'Port ' + port;

    // handle specific listen errors with friendly messages
    switch (error.code) {
        case 'EACCES':
            console.error(bind + ' requires elevated privileges');
            process.exit(1);
            break;
        case 'EADDRINUSE':
            console.error(bind + ' is already in use');
            process.exit(1);
            break;
        default:
            throw error;
    }
}

/**
 * Event listener for HTTP server "listening" event.
 */

function onListening() { //监听http服务运行
    let addr = server.address();
    let bind = typeof addr === 'string' ?
        'pipe ' + addr :
        'port ' + addr.port;
    debug('Listening on ' + bind); //服务开启成功输出url及端口
}
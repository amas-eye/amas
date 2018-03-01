let express = require('express')
let path = require('path')
let cors = require('cors') //跨域插件
let favicon = require('serve-favicon')
let proxy = require('express-http-proxy') //express http代理

let cookieParser = require('cookie-parser') //cookie解析中间件
let bodyParser = require('body-parser') //请求体中间件
let winston = require('winston'), //node日志插件
    expressWinston = require('express-winston') //express日志中间件 

let routes = require('./routes/index') //根路由
let jk = require('./routes/jk') //监控模块路由
let survey = require('./routes/survey') //总体概况路由
let alert = require('./routes/alert') //告警路由
let app = express() //app是express框架的根应用对象 根节点

// view engine setup
app.set('views', path.join(__dirname, 'views')) //设置视图目录
app.set('view engine', 'ejs') //设置视图引擎

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico'))) //网站logo路径
app.use(cors())
app.use(bodyParser.json()) //将请求体解析成json格式
app.use(bodyParser.urlencoded({ extended: false })) //解析url
app.use(cookieParser())
app.use('/argusapp', express.static(path.join(__dirname, 'app'))) //配置前端项目目录
app.use(express.static(path.join(__dirname, 'public'))) //配置静态资源目录


app.use(expressWinston.logger({ //请求日志
    transports: [
        new(winston.transports.File)({
            name: 'req-info',
            filename: './logs/req.log',
            level: 'info'
        })
    ]
}))

/*挂载路由*/
// app.use('/proxy', proxy('10.17.35.43:4242', { //内网
//     //   proxyReqPathResolver: function(req) {
//     //             //代理路径重写函数
//     //         console.info('代理',req)
//     //     return require('url').parse(req.url).path;
//     //   }
// }))
// app.use('/proxy8001', proxy('10.17.35.43:8001', { //内网 采集模块
//     //   proxyReqPathResolver: function(req) {
//     //             //代理路径重写函数
//     //         console.info('代理',req)
//     //     return require('url').parse(req.url).path;
//     //   }
// }))

app.use('/proxy', proxy('localhost:4242', { //服务器本地
    //   proxyReqPathResolver: function(req) {
    //             //代理路径重写函数
    //         console.info('代理',req)
    //     return require('url').parse(req.url).path;
    //   }
}))
app.use('/proxy8001', proxy('localhost:8001', { //服务器本地
    //   proxyReqPathResolver: function(req) {
    //             //代理路径重写函数
    //         console.info('代理',req)
    //     return require('url').parse(req.url).path;
    //   }
}))

// app.use('/proxy', proxy('192.168.0.253:4242', { //公司本部本地
//     //   proxyReqPathResolver: function(req) {
//     //             //代理路径重写函数
//     //         console.info('代理',req)
//     //     return require('url').parse(req.url).path;
//     //   }
// }))
// app.use('/proxy8001', proxy('192.168.0.253:8001', { //公司本部本地
//     //   proxyReqPathResolver: function(req) {
//     //             //代理路径重写函数
//     //         console.info('代理',req)
//     //     return require('url').parse(req.url).path;
//     //   }
// }))

// app.use('/proxy', proxy('http://183.3.139.134:4242', { //外网
//     //   proxyReqPathResolver: function(req) {
//     //             //代理路径重写函数
//     //         console.info('代理',req)
//     //     return require('url').parse(req.url).path;
//     //   }
// }))
// app.use('/proxy8001', proxy('http://183.3.139.134:8001', { //外网
//     //   proxyReqPathResolver: function(req) {
//     //             //代理路径重写函数
//     //         console.info('代理',req)
//     //     return require('url').parse(req.url).path;
//     //   }
// }))
app.use('/argus', routes)
app.use('/argus/jk', jk)
app.use('/argus/survey', survey)
app.use('/argus/alert', alert)

app.use(expressWinston.errorLogger({ //错误日志
    transports: [
        new(winston.transports.File)({
            name: 'sys-error',
            filename: './logs/err.log',
            level: 'error'
        })
    ]
}))

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    let err = new Error('Not Found')
    err.status = 404
    next(err)
})

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    //获取环境是开发环境返回错误给下面的节点 正式环境直接不返回
    app.use(function(err, req, res, next) {
        res.status(err.status || 500)
        res.render('error', {
            message: err.message,
            error: err
        })
    })
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {

    res.status(err.status || 500)
    res.render('error', {
        message: err.message,
        error: {}
    })
})


module.exports = app
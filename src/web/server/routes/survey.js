//概览路由

let express = require('express')
let router = express.Router()
let survey_services = require('../services/survey')


router.all(function(req, res, next) {
    //该路由下全请求

    console.info('请求', res)
    next(res)
})

router.get('/get_overall_health', function(req, res, next) {
    //获取健康度

    survey_services.get_overall_health().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})
router.get('/get_host_stat', function(req, res, next) {
    //获取主机信息数据

    survey_services.get_host_stat().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.get('/get_alert_stat', function(req, res, next) {
    //获取告警统计数据

    survey_services.get_alert_stat().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})
router.get('/get_metric_stat', function(req, res, next) {
    //获取指标统计数据

    survey_services.get_metric_stat().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})
router.get('/get_sys_resource', function(req, res, next) {
    //获取指所有Top5及基础资源使用量 

    survey_services.get_sys_resource().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.get('/get_mycharts', function(req, res, next) {
    //获取所有自定义指标图表

    survey_services.get_mycharts().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})
router.post('/add_mychart', function(req, res, next) {
    //添加概况指标图表

    // console.info('添加', req.body)
    let data = req.body

    // console.info('添加概况指标图表', data)
    survey_services.add_mychart(data.id).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })


})

router.post('/remove_mychart', function(req, res, next) {
    //删除概况指标图表

    // console.info('添加', req.body)
    let data = req.body
    survey_services.remove_mychart(data.id).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })


})


module.exports = router
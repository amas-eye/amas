//概览路由

let express = require('express')
let router = express.Router()
let alert_services = require('../services/alert')


router.all(function(req, res, next) {
    //该路由下全请求

    console.info('请求', res)
    next(res)
})

router.get('/get_warn_label', function(req, res, next) {
    //获取告警策略 列表

    let option = req.query

    alert_services.get_warn_label().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.get('/get_warn_strategy', function(req, res, next) {
    //获取告警策略 列表

    let option = req.query

    alert_services.get_warn_strategy(
        option.text,
        option.label,
        parseInt(option.page),
        parseInt(option.onepagecount)
    ).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.get('/get_strategy_count', function(req, res, next) {
    //获取告警策略数

    let option = req.query

    alert_services.strategycount(
        option.text,
        option.label
    ).then(rep => {
        res.send({ count: rep })
    }).catch(err => {
        res.send(err)
    })

})
router.post('/add_warn_strategy', function(req, res, next) {
    //添加告警策略
    let option = req.body.option

    // console.info('添加',option)
    alert_services.add_warn_strategy(option).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.post('/update_warn_strategy', function(req, res, next) {
    //更改告警策略
    let option = req.body.option
    alert_services.update_warn_strategy(option).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.post('/del_warn_strategy', function(req, res, next) {
    //删除告警策略
    let id = req.body.id
    alert_services.del_warn_strategy(id).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})
router.post('/toggle_warn', function(req, res, next) {
    //切换告警开关
    let option = req.body
    alert_services.toggle_warn(option.id).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})
router.get('/get_warn_history', function(req, res, next) {
    //获取告警历史

    let option = req.query

    alert_services.get_warn_history(
        option.text,
        parseInt(option.page),
        parseInt(option.onepagecount),
        JSON.parse(option.date)
    ).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.get('/get_history_count', function(req, res, next) {
    //获取告警历史数

    let option = req.query

    alert_services.historycount(
        option.text,
        JSON.parse(option.date)
    ).then(rep => {
        res.send({ count: rep })
    }).catch(err => {
        res.send(err)
    })

})



module.exports = router
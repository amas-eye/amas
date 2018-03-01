//监控路由

let express = require('express')
let router = express.Router()
let jk_services = require('../services/jk_services')


router.all(function(req, res, next) {
    //该路由下全请求

    console.info('请求', res)
    next(res)
})

router.get('/getdatetimeconfigs', function(req, res, next) {
    //获取视图数据获取时间配置

    let option = req.query

    jk_services.get_datetime_configs(option.viewid).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})
router.post('/updatedatetimeconfigs', function(req, res, next) {
    //更新视图数据获取时间配置

    let option = req.body

    jk_services.update_datetime_configs(option.viewid, option.datatimeconfig).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.get('/gettags', function(req, res, next) {
    //搜索视图

    // let option = req.query

    jk_services.gettages().then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})


router.get('/search', function(req, res, next) {
    //搜索视图

    let option = req.query

    console.info('查找时间', option) //查询参数

    jk_services.search(
        option.text,
        option.tag,
        parseInt(option.page),
        parseInt(option.onepagecount)
    ).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err)
    })

})

router.get('/viewcount', function(req, res, next) {
    //视图数统计
    let option = req.query
        // console.info('查找时间', option) //查询参数
    jk_services.viewcount(
        option.text,
        option.tag
    ).then(rep => {
        console.info('总数', req)
        res.send({ count: rep })
    }).catch(err => {
        res.send(err)
    })

})


router.post('/addview', function(req, res, next) {
    //添加视图

    console.info('发送消息', req.body.tags)

    jk_services.add(req.body).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err);
    })


})

router.post('/update', function(req, res, next) {
    //更新视图

    console.info('发送消息', req.body)
    let data = req.body

    jk_services.update(data.id, data.option).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err);
    })


})


router.post('/remove', function(req, res, next) {
    //删除视图

    console.info('发送消息', req.body)
    let data = req.body

    jk_services.remove(data.id).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err);
    })


})


router.post('/addchart', function(req, res, next) {
    //添加图表

    console.info('发送消息', req.body)
    let data = req.body

    jk_services.addchart(data.viewid, data.option).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err);
    })

})

router.post('/editchart', function(req, res, next) {
    //编辑图表

    // console.info('发送消息', req.body)
    let data = req.body

    jk_services.editchart(data.option).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err);
    })

})

router.get('/searchart', function(req, res, next) {
    //搜索获取图表

    // console.info('发送消息', req.body)
    let data = req.query

    jk_services.searchart(data.viewid).then(rep => {
        res.send(rep)
    }).catch(err => {
        res.send(err);
    })

})

module.exports = router
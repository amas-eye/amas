let connections = require('../db_connect') //连接
let mongoose = require('mongoose')
let alert = require('../models/alert') //告警模型
let bulkable = require('./bulkable')


module.exports = {
    get_warn_label: function() {
        //获取告警标签列表
        return new Promise((resolve, reject) => {

            let findQure = {

            }
            alert.labels.find(findQure).
            then(rep => {
                console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {

                reject(err)
            })

        })
    },
    get_warn_strategy: function(text, label, page, onepagecount) {
        //获取告警策略信息
        return new Promise((resolve, reject) => {

            //$regex 正则表达式查询

            let findQure = {
                "property.name": text == "" ? { $regex: '/*' } : { $regex: text, $options: 'i' }
            }
            if (!(label == "" || label == "all")) {
                findQure["property.labels"] = { $all: [label] }
            }

            console.info('调试', findQure)
            let skipnum = (page - 1) * onepagecount


            alert.strategy.find(findQure).limit(onepagecount).skip(skipnum).
            then(rep => { //查询
                console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })


        })
    },
    strategycount: function(text, label) {
        //策略数统计

        return new Promise((resolve, reject) => {


            let findQure = {
                "property.name": text == "" ? { $regex: '/*' } : { $regex: text, $options: 'i' }
            }
            if (!(label == "" || label == "all")) {
                findQure["property.labels"] = { $all: [label] }
            }

            alert.strategy.find(findQure).count().
            then(rep => { //查询
                // console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })

        })

    },
    add_warn_strategy: function(option) {
        //新增告警策略信息

        return new Promise((resolve, reject) => {

            let labels = option.property.labels //视图标签数组 

            let bulk = alert.labels.collection.initializeUnorderedBulkOp() //批量操作构造器（批量操作有点像事务，但是单个集合的事务）

            let newWarn = new alert.strategy(option)

            if (bulkable(bulk) && labels.length > 0) {
                console.info('调试', labels)
                labels.forEach(function(item) {
                    bulk.find({ label: item }).upsert().updateOne({ $set: { label: item } }) //更新没数据就更新数组做push操作
                })

                bulk.execute() //批量操作开始
            }



            newWarn.save(
                function(err) {
                    if (err) {
                        reject(err)
                    } else {
                        resolve('succeed')
                    }
                }
            )


        })
    },
    update_warn_strategy: function(option) {
        //更改告警策略信息
        return new Promise((resolve, reject) => {

            let newdata = { $set: option } //新数据
            let findQure = { //查询条件
                _id: option._id
            }

            let labels = option.property.labels //视图标签数组 

            let bulk = alert.labels.collection.initializeUnorderedBulkOp() //批量操作构造器（批量操作有点像事务，但是单个集合的事务）


            if (bulkable(bulk) && labels.length > 0) {
                console.info('调试', labels)
                labels.forEach(function(item) {
                    bulk.find({ label: item }).upsert().updateOne({ $set: { label: item } }) //更新没数据就更新数组做push操作
                })

                bulk.execute() //批量操作开始
            }

            alert.strategy.update(findQure, newdata, { "multi": true }, function(error) { //更新数据
                if (error) {
                    reject(error)
                } else {
                    resolve('succeed')
                }
            })


        })
    },
    del_warn_strategy: function(id) {
        //删除告警策略信息

        return new Promise((resolve, reject) => {
            let findQure = { //查询条件
                _id: id
            }

            alert.strategy.remove(findQure, function(error) { //删除数据
                if (error) {
                    reject(error)
                } else {
                    resolve('succeed')
                }
            })
        })
    },
    toggle_warn: function(id) {
        //切换告警开关
        return new Promise((resolve, reject) => {
            let findQure = { //查询条件
                _id: id
            }

            alert.strategy.updateOne(findQure, { $set: { status: 'ok' } }).then(req => {
                resolve(req)
            }).catch(err => {
                reject(err)
            })
        })
    },
    get_warn_history: function(text, page, onepagecount, date) {
        //获取告警策略历史信息
        return new Promise((resolve, reject) => {

            //$regex 正则表达式查询

            let findQure = {
                strategy_name: text == "" ? { $regex: '/*' } : { $regex: text, $options: 'i' }
            }
            if (date.start != "" || date.end != "") { //判断时间查询条件
                if (date.end == "") {
                    findQure.alert_time = {
                        $gte: parseInt(date.start),
                    }
                } else if (date.start == "") {
                    findQure.alert_time = {
                        $lte: parseInt(date.end),
                    }
                } else {
                    findQure.alert_time = {
                        $gte: parseInt(date.start),
                        $lte: parseInt(date.end)
                    }
                }
            }

            //console.info(findQure)
            let skipnum = (page - 1) * onepagecount


            alert.history.find(findQure).limit(onepagecount).skip(skipnum).
            then(rep => { //查询
                console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })


        })
    },
    historycount: function(text, date) {
        //历史记录数统计

        return new Promise((resolve, reject) => {
            let findQure = {
                strategy_name: text == "" ? { $regex: '/*' } : { $regex: text, $options: 'i' },
            }

            if (date.start != "" || date.end != "") { //判断时间查询条件
                if (date.end == "") {
                    findQure.alert_time = {
                        $gte: parseInt(date.start),
                    }
                } else if (date.start == "") {
                    findQure.alert_time = {
                        $lte: parseInt(date.end),
                    }
                } else {

                    findQure.alert_time = {
                        $gte: parseInt(date.start),
                        $lte: parseInt(date.end)
                    }
                }
            }



            alert.history.find(findQure).count().
            then(rep => { //查询
                // console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })

        })

    },

}
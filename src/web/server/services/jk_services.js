//消息服务
let connections = require('../db_connect') //连接
let mongoose = require('mongoose')
let moment = require('moment')
let jk_viewlists = require('../models/jk_viewlists') //视图模型
let jk_tags = require('../models/jk_tags') //视图tag模型
let jk_charts = require('../models/jk_charts') //图表模型
let bulkable = require('./bulkable')

module.exports = {
    get_datetime_configs: function(id) {
        //获取视图时间日期配置
        return new Promise((resolve, reject) => {
            let findQure = {
                viewid: id
            }
            jk_charts.jk_datatime_configs.find(findQure).then(rep => {
                console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                reject(err)
            })
        })
    },
    update_datetime_configs: function(id, option) {
        //更新视图时间日期配置 (option时间配置)
        return new Promise((resolve, reject) => {
            let findQure = {
                viewid: id
            }
            jk_charts.jk_datatime_configs.updateOne(findQure, { $set: option }, { upsert: true }).then(rep => {
                console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                reject(err)
            })
        })
    },
    gettages: function() {
        //获取视图标签列表
        return new Promise((resolve, reject) => {

            //$regex 正则表达式查询

            //console.info(moment(endtime).add(1, 'days').format())


            let findQure = {
                // name: text == "" ? { $regex: '/*' } : { $regex: text, $options: 'i' },
                // tag: tag == "" ? { $regex: '/*' } : tag,

            }

            //console.info(findQure)

            jk_tags.find(findQure).
            then(rep => { //查询
                // console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })

        })
    },

    viewcount: function(text, tag) {
        //视图数统计

        return new Promise((resolve, reject) => {
            let findQure = {
                name: text == "" ? { $regex: '/*' } : { $regex: text, $options: 'i' },
                tags: tag == "" ? { $regex: '/*' } : { $all: [tag] }
            }


            jk_viewlists.find(findQure).count().
            then(rep => { //查询
                // console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })

        })

    },
    search: function(text, tag, page, onepagecount) {
        //查询监控列表
        return new Promise((resolve, reject) => {

            //$regex 正则表达式查询

            //console.info(moment(endtime).add(1, 'days').format())

            let findQure = {
                name: text == "" ? { $regex: '/*' } : { $regex: text, $options: 'i' }
            }
            if (!(tag == "" || tag == "all")) {
                findQure.tags = { $all: [tag] }
            }

            //console.info(findQure)
            let skipnum = (page - 1) * onepagecount


            jk_viewlists.find(findQure).limit(onepagecount).skip(skipnum).
            then(rep => { //查询
                console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })


        })

    },
    add: function(option) {
        //添加监控视图进列表

        return new Promise((resolve, reject) => {
            // option.rdj='666'
            let tags = option.tags //视图标签数组 
            let bulk = jk_tags.collection.initializeUnorderedBulkOp() //批量操作构造器（批量操作有点像事务，但是单个集合的事务）

            let newview = new jk_viewlists({
                name: option.name, //视图名称
                tags: tags, //标签数组
                creater: option.creater, //创建者
            })


            console.info('标签', tags)

            if (bulkable(bulk) && tags.length > 0) {
                tags.forEach(function(item) {
                    // bulk.find( { tag: item } ).upsert().updateOne( { $set:{ tag: item }, $push: { viewids:newview._id } } ) //更新没数据就更新数组做push操作
                    bulk.find({ tag: item }).upsert().updateOne({ $set: { tag: item } }) //更新没数据就更新数组做push操作
                })

                bulk.execute() //批量操作开始
            }
            newview.save(
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
    update: function(id, option) {
        //编辑更改监控视图进列表


        return new Promise((resolve, reject) => {

            let findQure = { //查询条件
                _id: id
            }
            let tags = option.tags //视图标签数组 

            let bulk = jk_tags.collection.initializeUnorderedBulkOp() //批量操作构造器（批量操作有点像事务，但是单个集合的事务）


            let newdata = { $set: option } //新数据

            if (bulkable(bulk) && tags.length > 0) {
                tags.forEach(function(item) {
                    // bulk.find( { tag: item } ).upsert().updateOne( { $set:{ tag: item }, $push: { viewids:newview._id } } ) //更新没数据就更新数组做push操作
                    bulk.find({ tag: item }).upsert().updateOne({ $set: { tag: item } }) //更新没数据就更新数组做push操作
                })

                bulk.execute() //批量操作开始
            }


            jk_viewlists.update(findQure, newdata, { "multi": true }, function(error) { //更新数据
                if (error) {
                    reject(error)
                } else {
                    resolve('succeed')
                }
            })
        })
    },
    remove: function(id) {
        //删除监控视图


        return new Promise((resolve, reject) => {

            let findQure = { //查询条件
                _id: id
            }

            jk_viewlists.remove(findQure, function(error) { //删除数据
                if (error) {
                    reject(error)
                } else {
                    resolve('succeed')
                }
            })
        })
    },
    addchart: function(viewid, option) {
        //添加图表

        return new Promise((resolve, reject) => {

            let nomalinfo = option.nomalinfo //基础信息
            let pfm_index = option.pfm_index //性能指标
            let ystyle = option.ystyle //y轴样式

            nomalinfo.viewid = viewid
            let newchart_nomals = new jk_charts.jk_chart_nomals(nomalinfo)
            pfm_index.forEach(function(item) {
                let id = mongoose.Types.ObjectId() //手动生成id
                item._id = id
                newchart_nomals.xnzbs.push(id) //同步关联id
                item.chartid = newchart_nomals._id //同步关联id

            })
            console.info('性能指标', pfm_index)
            ystyle.chartid = newchart_nomals._id //同步关联id
            let newchart_ystyle = new jk_charts.jk_chart_ytypes(ystyle)
            console.info('y轴样式', ystyle)
            newchart_nomals.yconfig = newchart_ystyle._id //同步关联id
            console.info('基础信息', newchart_nomals)

            let caozuo = [ //所有操作
                newchart_nomals.save(),
                newchart_ystyle.save(),
                jk_charts.jk_chart_xnzbs.insertMany(pfm_index)
            ]

            Promise.all(caozuo).then(
                function(posts) {
                    resolve('suceed')
                }).catch(
                function(reason) {
                    reject(reason)
                });



        })
    },
    editchart: function(option) {
        //编辑图表


        return new Promise((resolve, reject) => {

            let chartid = option.nomalinfo._id

            let nomalinfo = {
                    title: option.nomalinfo.title,
                    type: option.nomalinfo.type,
                    xnzbs: []
                } //基础信息
            let pfm_index = option.pfm_index //性能指标
            let ystyle = option.ystyle //y轴样式


            nomalinfo.xnzbs = [] //清空性能指标关联id

            pfm_index.forEach(function(item) {
                let id = mongoose.Types.ObjectId() //手动生成id
                item._id = id
                nomalinfo.xnzbs.push(id) //同步关联id
                item.chartid = chartid //同步关联id

            })

            console.info('编辑图表', option)
                //直接删了再加过比更改简单

            let pfm_update = function() { //性能指标更新
                return new Promise((resolve, reject) => {
                    jk_charts.jk_chart_xnzbs.deleteMany({ chartid: chartid }).then(
                        res => {
                            jk_charts.jk_chart_xnzbs.insertMany(pfm_index).then(
                                res => {
                                    resolve('succeed')
                                }
                            ).catch(
                                err => {
                                    console.info('操作结果2', err)
                                    reject(err)
                                }
                            )
                        }
                    ).catch(
                        err => {
                            console.info('操作结果1', err)
                            reject(err)
                        })

                })
            }
            console.info('调试', chartid)
            let caozuo = [ //所有操作
                jk_charts.jk_chart_nomals.update({ _id: chartid }, { $set: nomalinfo }, { "multi": true }),
                jk_charts.jk_chart_ytypes.update({ chartid: chartid }, { $set: ystyle }, { "multi": true }),
                pfm_update()
            ]


            Promise.all(caozuo).then(
                function(posts) {
                    resolve(posts)
                }).catch(
                function(reason) {
                    console.info('操作结果all', reason)
                    reject(reason)
                });



        })
    },
    searchart: function(viewid) {
        //查询图表数据
        return new Promise((resolve, reject) => {
            let findQure = {
                viewid: viewid
                    // tag: tag == "" ? { $regex: '/*' } : tag,

            }

            //console.info(findQure)

            jk_charts.jk_chart_nomals.find(findQure, { '__v': 0 }).populate('xnzbs yconfig', '-_id -__v').
            then(rep => { //查询
                // console.info('查询结果', rep)
                resolve(rep)
            }).catch(err => {
                //console.info('查询结果', err)
                reject(err)
            })

        })
    }


    // check: function(ids, status) {
    //     //审核消息
    //     return new Promise((resolve, reject) => {

    //         // let message = new jk_viewlists({
    //         //     title: option.title,
    //         //     stype: option.stype,
    //         //     content: option.content,
    //         // })
    //         let obids = []

    //         ids.map(
    //             (id) => {
    //                 obids.push({
    //                     _id: mongoose.Types.ObjectId(id) //把字符串id转为objectid
    //                 })
    //             }
    //         )



    //         jk_viewlists.update({ "$or": obids }, { $set: { status: status } }, { "multi": true },
    //             err => {
    //                 if (err) {
    //                     reject(err)
    //                 } else {
    //                     resolve('审核成功')

    //                 }
    //             }
    //         )
    //     })

    // }
}
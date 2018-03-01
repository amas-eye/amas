//登录服务
let users = require('../models/users') //用户模型

module.exports = () => {
    return new Promise((resolve, reject) => {
        if (users != null) {
            console.info('用户模型', users)
            resolve('成功')
        } else {
            reject('失败')
        }
    })
}
//get的基础自定义
import { Loading } from 'element-ui'; //加载动效
import { Message } from 'element-ui'; //信息弹窗
import { HOST } from 'service/HOST'

//import vue from 'vue'

function err_dispose(err) {
    //异常处理函数
    if (err.status == 500) {

        Message({
            message: '请求失败请检查网络',
            type: 'error',
            showClose: true
        })

    } else {

        Message({
            message: '未知错误',
            type: 'error',
            showClose: true
        })

    }
}


//import qs from 'qs'; //请求参数处理库
import axios from 'axios' //请求库
//axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'; //请求头
axios.defaults.baseURL = HOST; //url公共前缀

export default {
    get: function(url, info) {
        //get请求    
        return new Promise(function(resolve, reject) {
            let currentLoad = Loading.service({ //加载特效
                    text: '加载中。。。'
                })
                //get请求
            axios.get(url, { params: info }).then(
                res => {
                    resolve(res)
                        // console.log(res)
                    currentLoad.close()

                }
            ).catch(
                err => {
                    err_dispose(err) //错误处理
                    reject(err)
                    currentLoad.close()
                }
            )

        })

    },
    post: function(url, info) {
        //post请求
        return new Promise(function(resolve, reject) {

            let currentLoad = Loading.service({ //加载特效
                text: '加载中。。。'
            })

            //get请求
            axios.post(url, info, { //qs序列化参数 做成stringformdate格式(java后台需要)
                headers: { //头部配置
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    // 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' //(java后台需要)
                },
                // params: info,
                // paramsSerializer: function(params) {
                //     return Qs.stringify(params, { arrayFormat: 'brackets' })
                // },
            }).then(
                res => {
                    resolve(res) //解析结果为json
                    currentLoad.close()
                }
            ).catch(
                err => {
                    currentLoad.close()
                    err_dispose(err)
                    reject(err)
                }
            )
        })

    }
}

// export default function(type, url, info) {
//     return new Promise(function(resolve, reject) {

//         Indicator.open({
//             text: '加载中...',
//             spinnerType: 'fading-circle'
//         })

//         if (type == 'get') {
//             //get请求
//             axios.get(url, { params: info }).then(
//                 res => {
//                     resolve(res)
//                         // console.log(res)
//                     Indicator.close()

//                 }
//             ).catch(
//                 err => {
//                     err_dispose(err) //错误处理
//                     reject(err)
//                     Indicator.close()
//                 }
//             )
//         } else if (type == 'post') {
//             //post请求
//             axios.post(url, qs.stringify(info), {
//                 headers: {
//                     'Accept': 'application/json, text/javascript, */*; q=0.01',
//                     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
//                 },
//                 // params: info,
//                 // paramsSerializer: function(params) {
//                 //     return Qs.stringify(params, { arrayFormat: 'brackets' })
//                 // },
//             }).then(
//                 res => {
//                     resolve(res) //解析结果为json
//                     Indicator.close()
//                 }
//             ).catch(
//                 err => {
//                     Indicator.close()
//                     err_dispose(err)
//                     reject(err)
//                 }
//             )

//         }

//     })
// }
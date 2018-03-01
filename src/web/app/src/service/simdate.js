import moment from 'moment' //时间处理库(建议后台做时间处理)
// console.log(moment().days(-1).format('Y-M-D'))



export default {

    YMD: function(date) {
        //日期转化为YMD模式(2017/07/03-11:09:50)
        return moment(date).format('Y-M-D')
    },
    SJCtoTime: function(date) {
        //时间戳转默认时间格式
        // console.log(date)
        if (date != '' && date != null && typeof(date) != "undefined") {
            // console.info('时间戳', date)
            return moment.unix(date).format('Y-M-D H:mm:ss')
        } else {
            return ''
        }
    },
    TimetoSJC: function(date) {
        //时间转时间戳
        if (date != '' && date != null && typeof(date) != "undefined") {
            return moment(date).format('X')
        } else {
            return ''
        }
    },
    TMDTime: function(date) {
        //热力图时间格式

        return moment(date).format('Y-M-D H:mm:ss')
    },
    todayTime: function() {
        //今天
        return moment().format('Y-M-D H:mm')

    },

    min5_ago: function() {
        //5分钟前
        return moment().subtract('minutes', 5).format('Y-M-D H:mm:ss')
    },
    min10_ago: function() {
        //10分钟前
        return moment().subtract('minutes', 10).format('Y-M-D H:mm:ss')
    },
    min30_ago: function() {
        //30分钟前
        return moment().subtract('minutes', 30).format('Y-M-D H:mm:ss')
    },
    hour1_ago: function() {
        //1小时前
        return moment().subtract('hours', 1).format('Y-M-D H:mm:ss')
    },
    hour6_ago: function() {
        //6小时前
        return moment().subtract('hours', 6).format('Y-M-D H:mm:ss')
    },
    hour12_ago: function() {
        //12小时前
        return moment().subtract('hours', 12).format('Y-M-D H:mm:ss')
    },
    day1_ago: function() {
        //1天前
        return moment().subtract('days', 1).format('Y-M-D H:mm:ss')
    },
    day7_ago: function() {
        //7天前
        return moment().subtract('days', 6).format('Y-M-D H:mm:ss')
    },
    day15_ago: function() {
        //15天前
        return moment().subtract('days', 14).format('Y-M-D H:mm:ss')
    },
    today: function() {
        //今天
        return moment().format('Y-M-D H:mm:ss')
    },
    yesterday: function() {
        //昨天
        return moment().subtract('days', 1).format('Y-M-D H:mm:ss')
    },
    aweek: function() {
        //一周内
        return {
            start: moment().days(-7).format('Y-M-D'),
            end: moment().format('Y-M-D')
        }
    },
    amounth: function() {
        //一月内
        return {
            start: moment().days(-30).format('Y-M-D'),
            end: moment().format('Y-M-D')
        }
    }

}
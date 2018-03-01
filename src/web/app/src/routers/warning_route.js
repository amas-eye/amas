// const hello_view = resolve => require(['view/hello.vue'], resolve) //组件异步懒加载写法
import warning_view from 'view/warning'
export const warning_route = { //告警列表页

    path: 'warning',
    component: warning_view

}
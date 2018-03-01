// const hello_view = resolve => require(['view/hello.vue'], resolve) //组件异步懒加载写法
import monitorView from 'view/monitorView'
export const monitor_route = { //进入监控视图（图表）

    path: 'monitorView',
    component: monitorView

}
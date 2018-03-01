// const hello_view = resolve => require(['view/hello.vue'], resolve) //组件异步懒加载写法
import collect_view from 'view/collect'
export const collect_route = { //采集列表页

    path: 'collect',
    component: collect_view

}
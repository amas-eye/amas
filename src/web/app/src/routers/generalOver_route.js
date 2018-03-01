// const hello_view = resolve => require(['view/hello.vue'], resolve) //组件异步懒加载写法
import generalOverview_view from 'view/generalOverview'
export const generalOver_route = { //视图列表页

    path: 'generalOverview',
    component: generalOverview_view

}
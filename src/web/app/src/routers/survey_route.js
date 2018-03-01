// const hello_view = resolve => require(['view/hello.vue'], resolve) //组件异步懒加载写法
import survey_view from 'view/survey'
export const survey_route = { //总体概况路由

    path: 'survey',
    component: survey_view

}
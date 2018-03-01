// const hello_view = resolve => require(['view/hello.vue'], resolve) //组件异步懒加载写法
import navBar_view from 'view/navBar'
import { survey_route } from './survey_route'
import { generalOver_route } from './generalOver_route'
import { error_route } from './error_route'
import { monitor_route } from './monitor_route'
import { warning_route } from './warning_route'
import { collect_route } from './collect_route'

export const navBar_route = { //navBar 主导航
    path: '/navBar',
    component: navBar_view,
    children: [
        survey_route,
        generalOver_route,
        monitor_route,
        warning_route,
        collect_route,
        error_route
    ]
}
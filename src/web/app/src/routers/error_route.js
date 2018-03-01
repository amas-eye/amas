//const login_view = resolve => require(['view/login.vue'], resolve) //组件异步懒加载写法
import error_view from 'view/error' //错误页面

export const error_route = {
    path: 'error',
    component: error_view
}
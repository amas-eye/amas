//const login_view = resolve => require(['view/login.vue'], resolve) //组件异步懒加载写法
import login_view from 'view/login'

export const login_route = {
    path: '/login',
    component: login_view
}
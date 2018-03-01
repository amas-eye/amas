// 根路由配置
import { login_route } from './login_route'
import { navBar_route } from './navBar_route'

// import { error_route } from './error_route'


const routes = [
    login_route,
    navBar_route,
    // error_route,
    { path: '*', redirect: '/navBar/generalOverview' } //重定向
]

export const router_config = { //路由配总配置
    // mode: 'history', //h5路由模式
    routes: routes //路由地址配置数组
}
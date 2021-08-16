import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('@/views/home')
    },
    {
        path: '/posts',
        name: 'posts',
        component: () => import('@/views/posts')
    },
    {
        //TODO delete in future
        path: '/check',
        name: 'check',
        component: () => import('@/views/check')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('@/views/login')
    },
    {
        path: '/sign_up',
        name: 'sign_up',
        component: () => import('@/views/sign_up')
    },
    {
        path: '/forgot_password',
        name: 'forgot_password',
        component: () => import('@/views/forgot_password')
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router

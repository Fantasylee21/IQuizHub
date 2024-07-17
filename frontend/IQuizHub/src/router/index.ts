import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')

const routes: Array<RouteRecordRaw> = [
	{
		path: '/staging',
		name: 'MainStaging',
		component: MainStaging,
	}
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to, from, next) => {
	sessionStorage.setItem('preRoute', to.path)
	next()
})

export default router

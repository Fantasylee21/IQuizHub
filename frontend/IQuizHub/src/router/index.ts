import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')
const QuestionSheet = () => import('@/views/QuestionSheet.vue')
const LoginRegister = () => import('@/views/LoginRegister.vue')
const MyTest = () => import('@/views/MyTest.vue')

const routes: Array<RouteRecordRaw> = [
	{
		path: '/staging',
		name: 'MainStaging',
		component: MainStaging,
	},
	{
		path: '/question-sheet',
		name: 'QuestionSheet',
		component: QuestionSheet,
	},
	{
		path: '/loginRegister',
		name: 'LoginRegister',
		component: LoginRegister,
	},
	{
		path: '/test',
		name: 'test',
		component: MyTest,
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

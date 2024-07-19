import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')
const QuestionSheet = () => import('@/views/QuestionSheet.vue')
const LoginRegister = () => import('@/views/LoginRegister.vue')
const UserCenter = () => import('@/views/UserCenter.vue')
const QuestionBank = () => import('@/views/QuestionBank.vue')
const GroupPage = () => import('@/views/GroupPage.vue')

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
		path: '/userCenter',
		name: 'UserCenter',
		component: UserCenter,
	},
	{
		path: '/loginRegister',
		name: 'LoginRegister',
		component: LoginRegister,
	},
	{
		path: '/questionBank',
		name: 'QuestionBank',
		component: QuestionBank,
	},
	{
		path: '/groupPage',
		name: 'GroupPage',
		component: GroupPage,
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

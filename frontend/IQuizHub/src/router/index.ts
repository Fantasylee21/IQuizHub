import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')
const QuestionSheet = () => import('@/views/QuestionSheet.vue')
const LoginRegister = () => import('@/views/LoginRegister.vue')

const UserCenter = () => import('@/views/UserCenter.vue')
const QuestionBank = () => import('@/views/QuestionBank.vue')
const GroupPage = () => import('@/views/GroupPage.vue')
const QuestionDetail = () => import('@/views/QuestionDetail.vue')
const QuestionEditor = () => import('@/views/QuestionEditor.vue')
const SheetDetail = () => import('@/views/SheetDetail.vue')
const GroupDetail = () => import('@/views/GroupDetail.vue')
const SheetEditor = () => import('@/views/SheetEditor.vue')
const MySheet = () => import('@/views/MySheet.vue')

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
		props: true
	},
	{
		path: '/question-detail/:id',
		name: 'QuestionDetail',
		component: QuestionDetail,
		props: true
	},
	{
		path: '/sheet-detail/:id',
		name: 'SheetDetail',
		component: SheetDetail,
		props: true
	},
	{
		path: '/question-editor',
		name: 'QuestionEditor',
		component: QuestionEditor,
	},
	{
		path: '/groupDetail/:id',
		name: 'GroupDetail',
		component: GroupDetail,
		props: true
	},
	{
		path: '/sheet-editor/:id',
		name: 'SheetEditor',
		component: SheetEditor,
		props: true
	},
	{
		path: '/my-sheet',
		name: 'MySheet',
		component: MySheet
	}
]

const router = createRouter({
	// history: createWebHistory(process.env.BASE_URL),
	history: createWebHistory(),
	routes,
})

router.beforeEach((to, from, next) => {
	sessionStorage.setItem('preRoute', to.path)
	next()
})

export default router

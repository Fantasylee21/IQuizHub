import axios from 'axios'
import env from '@/utils/env'
import {ElMessage} from "element-plus";
import router from "@/router";
import {useProfileStore} from "@/store/profile";

const profile = useProfileStore();

const api = axios.create({
	baseURL: env.backEnd,
	withCredentials: false,
	timeout: 50000,
})

// 延时函数
function delay(ms: any) {
	return new Promise((resolve) => setTimeout(resolve, ms))
}

export default {
	getNowUser: async function (params: { id: string }) {
		return (await api.get(`users/users/` + params.id + '/', {
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('token')}`,
			}
		})).data
	},

	ask: async function (params: object) {
		return (await api.post(`ai/ask/`, params)).data.result;
	},

	uploadQuestion: async function (params: object) {
		try {
			const res = (await api.post(`api/question/upload/`, params, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			})).data;
			return res;
		} catch (e) {
			return null;
		}

	},

	register: async function (params: { username: string; email: string; password: string }) {
		try {
			const isSuccess = (await api.post(`users/register/`, params)).status == 201
			if (isSuccess) {
				ElMessage.success('注册成功')
				const ret = await this.login({
					username: params.username,
					password: params.password,
				})
				if (ret) {
					ElMessage.success('登录成功')
					profile.updateProfile(ret);
					setTimeout(() => {
						router.push('/staging')
					}, 500)
				}
			} else ElMessage.error('注册失败')
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	},

	login: async function (params: { username: string; password: string }) {
		try {
			const user = await api.post(`users/login/`, params)
			localStorage.setItem('token', user.data.token)
			localStorage.setItem('refresh', user.data.refresh)
			return this.getNowUser({id: user.data.id.toString()})

		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error[0])
			return null
		}
	},
}
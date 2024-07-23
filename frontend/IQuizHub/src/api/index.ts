import axios from 'axios'
import env from '@/utils/env'
import {ElMessage} from "element-plus";
import router from "@/router";
import {useProfileStore} from "@/stores/profile";

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

	checkQuestion: async function (params: object) {
		return (await api.post(`api/question/check/question/`, params, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('token')}`,
			}
		})).data;
	},

	getAllQuestions: async function (params : {pageNumber: number}) {
		try {
			const url = `api/question/get/questions/?page=${params.pageNumber}`;
			const response = await api.get(url, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			});
			return response.data;
		} catch (e) {
			return null;
		}
},

	search: async function (params: {pageNumber : number, Tags: string[], keyword: string}) {
    try {
				console.log('tags----------------', params.Tags)
        const res = (await api.get(`api/question/query/question/`, {
						params: {
							'page': params.pageNumber,
							'tags': params.Tags,
							'title': params.keyword,
						},
            headers: {
                'Content-Type' : 'application/json',
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            }
        })).data;
				console.log(`output->res`, res)
        return res;
    } catch (e) {
        return null;
    }
},

	getQuestionDetail: async function (id: string) {
		return (await api.get(`api/question/detail/${id}/`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('token')}`,
			}
		})).data
	},

	getAllQuestionSheet: async function (params: {pageNumber: number}) {
		try {
			const url = `api/question/questiongroup/all/?page=${params.pageNumber}`;
			const response = await api.get(url, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			});
			return response.data;
		} catch (e) {
			return null;
		}
	},

	searchQuestionSheet: async function (params: {pageNumber: number, keyword: string, type: number}) {
		try {
			const url = `api/question/guestiongroup/query/?page=${params.pageNumber}&title=${params.keyword}&type=${params.type}`;
			const response = await api.get(url, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			});
			return response.data;
		} catch (e) {
			return null;
		}
	}
}
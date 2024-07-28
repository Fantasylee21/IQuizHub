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

	getAllQuestions: async function (params: { pageNumber: number }) {
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

	search: async function (params: { pageNumber: number, Tags: string[], keyword: string, type: string }) {
		try {
			console.log('tags----------------', params.Tags)
			const res = (await api.get(`api/question/query/question/`, {
				params: {
					'page': params.pageNumber,
					'tags': params.Tags,
					'title': params.keyword,
					'type': params.type
				},
				headers: {
					'Content-Type': 'application/json',
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

	getAllQuestionSheet: async function (params: { pageNumber: number }) {
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

	searchQuestionSheet: async function (params: { pageNumber: number, keyword: string, type: number }) {
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
	},

	getUserInformation: async function (params: { id: number }) {
		try {
			const response = await api.get(`users/users/${params.id}/`, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			});
			console.log(`output->response`, response)
			return response.data;
		} catch (e) {
			console.log(`output->e`, e)
			return null;
		}
	},

	uploadIntroduction: async function (params: { id: number, introduction: string }) {
		try {
			const response = await api.post(`users/${params.id}/introduction/`, {
				introduction: params.introduction
			}, {
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

	uploadAvatar: async function (params: { id: number, avatar: File }) {
		try {
			const formData = new FormData();
			formData.append('avatar', params.avatar);

			const response = await api.post(`users/${params.id}/avatar/upload/`, formData, {
				headers: {
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			});

			return response.data;
		} catch (e) {
			return null;
		}
	},

	getSheetDetail: async function (id: string) {
		return (await api.get(`api/question/questiongroup/detail/${id}/`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('token')}`,
			}
		})).data
	},

	deleteQuestionGroup: async function (params: { id: number }) {
		try {
			const response = await api.delete(`api/question/questiongroup/delete/${params.id}/`, {
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

	uploadQuestionGroup: async function (prams: {
		questions: Array<number>,
		users: Array<number>,
		title: string,
		content: string,
		is_all: boolean
	}) {
		try {
			console.log(`output->prams`, prams)
			const response = await api.post(`api/question/questiongroup/upload/`, prams, {
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

	deleteQuestion: async function (params: { id: number }) {
		try {
			const response = await api.delete(`api/question/delete/${params.id}/`, {
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

	getAllUsers: async function () {
		try {
			const response = await api.get(`users/detail/`, {
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

	collect: async function (params: object) {
		try {
			const response = await api.post(`api/question/favorite/`, params, {
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

	getComments: async function (params: { page: number, id: number }) {
		try {
			const response = await api.get(`users/comment/query/?page=${params.page}&question=${params.id}`, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			});
			return response.data;
		} catch (e) {
			return null
		}
	},

	postComment: async function (params: object) {
		try {
			const response = await api.post(`users/comment/upload/`, params, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('token')}`,
				}
			});
			return response.data;
		} catch (e) {
			return null
		}
	},


	getAllGroups: async function () {
		try {
			const response = await api.get(`/api/question/usergroup/detail/`, {
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

	searchGroupDetail: async function (params: { title : string ,type: string}) {
		return (await api.get(`api/question/usergroup/query/`, {
			params: {
				'title': params.title,
				'type': params.type
			},
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('token')}`,
			}
		})).data
	},

	getGroupDetail: async function (params : { usergroup_id: string }) {
		return (await api.get(`api/question/usergroup/detail/${params.usergroup_id}/`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('token')}`,
			}
		})).data
	},

	createGroup: async function (params: { title: string, content: string, type: string }) {
		try {
			const response = await api.post(`api/question/usergroup/upload/`, params, {
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

	joinGroup: async function (params: { usergroup_id: string }) {
		try {
			const response = await api.post(`/api/question/usergroup/addmember/${params.usergroup_id}/`, {}, {
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

	uploadcomment: async function (params: { usergroup: number, comment: string }) {
		try {
			const response = await api.put(`api/question/usergroup/uploadcomment/`, {
				usergroup: params.usergroup,
				comment: params.comment
			}, {
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

}
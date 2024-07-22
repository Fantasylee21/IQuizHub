import axios from 'axios'
import env from '@/utils/env'

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
	ask: async function (params: object) {
		return (await api.post(`ai/ask/`, params)).data.result;
	},

	uploadQuestion: async function (params: object) {
		try {
			const res = (await api.post(`api/question/upload/`, params, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxNTQ0OTkzLCJpYXQiOjE3MjE1NDEzOTMsImp0aSI6ImY4ZWEyYTMxNDRjNDQ4ZjBiZDVjMTc3NmE0OGQ2NzdmIiwidXNlcl9pZCI6M30.KxDWHftmc591wcDn36NSbUlsTvCFtx4DtApN762uHFc`,
				}
			})).data;
			return res;
		} catch (e) {
			return null;
		}

	},

	getAllQuestions: async function () {
		try {
			const res = (await api.get(`api/question/get/questions/`)).data;
			return res;
		} catch (e) {
			return null;
		}
	},

	search: async function (keyword: string, Tags: string[]) {
		try {
			const res = (await api.get(`api/question/search/${keyword}`, {
				headers: {
					'Content-Type' : 'application/json',
				}
			})).data;
			return res;
		} catch (e) {
			return null;
		}
	},

}
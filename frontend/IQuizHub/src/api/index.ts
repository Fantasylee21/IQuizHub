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
}
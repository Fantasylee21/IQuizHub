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

	login: async function (params: object) {
        try {
            const res = (await api.post(`login/`, params)).data;
            localStorage.setItem('token', res.token);
            return res;
        } catch (e) {
            return null;
        }
    },

    register: async function (params: object) {
        try {
            const res = (await api.post(`register/`, params)).data;
            localStorage.setItem('token', res.token);
            return res;
        } catch (e) {
            return null;
        }
    },
}
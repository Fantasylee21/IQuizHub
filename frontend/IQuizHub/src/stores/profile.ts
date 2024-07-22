import {defineStore} from 'pinia'

interface ProfileState {
	username: string
	id: string
	mobile: string
	email: string
	avatar: string
	companyIds: Array<number>
	did: string
	keywords: Array<Array<string>>
}

export const useProfileStore = defineStore('profile', {
	state: (): ProfileState => ({
		username: '',
		id: '0',
		mobile: '',
		email: '',
		avatar: '',
		companyIds: [],
		did: '0',
		keywords: [],
	}),

	actions: {
		updateProfile(profile: {
			username: string
			id: string
			mobile: string
			email: string
			avatar: string
			company_ids: Array<number>
			keywords: Array<Array<string>>
		}) {
			this.username = profile.username
			this.id = profile.id
			this.mobile = profile.mobile
			this.email = profile.email
			this.avatar = profile.avatar
			this.companyIds = profile['company_ids']
			this.keywords = profile['keywords']
		},
	},

	persist: {
		key: 'profile-store',
		storage: window.sessionStorage,
		paths: ['username', 'id', 'mobile', 'email', 'avatar', 'companyIds'],
	},
})
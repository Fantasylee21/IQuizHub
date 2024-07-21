import {createApp} from 'vue'
import {createPinia} from 'pinia'

import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import '@/assets/reset.css'
import 'element-plus/dist/index.css'

import ElementTiptapPlugin from 'element-tiptap-vue3-fixed';
// import ElementTiptap's styles
import 'element-tiptap-vue3-fixed/lib/style.css';

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(ElementTiptapPlugin)

app.mount('#app')

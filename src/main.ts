import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import  "./components/index.css"
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
//@ts-ignore
createApp(App).use(store).use(router).use(ElementPlus).mount('#app')

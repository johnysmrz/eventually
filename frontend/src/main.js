import { createApp } from 'vue'
import App from './App.vue'

import { createPinia } from 'pinia'
import router from './router.js'
import 'primeicons/primeicons.css'


const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')


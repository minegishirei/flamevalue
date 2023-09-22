import { createApp } from 'vue'
import VueGtag from "vue-gtag";
import App from './App.vue'
import router from './router'

//createApp(App).mount('#app')
const app = createApp(App).use(router)
app.use(VueGtag, {
  config: { id: "G-Q2V7S4KFFD" }
})
app.mount('#app')
// G-Q2V7S4KFFD
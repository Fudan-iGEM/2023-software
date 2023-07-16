import Vue from 'vue'
import login from './login.vue'
import "@/assets/font/font.css"

Vue.config.productionTip = false

new Vue({
    render: h => h(login),
}).$mount('#app')
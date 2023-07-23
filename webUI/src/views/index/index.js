import Vue from 'vue'
import index from './index.vue'
import "@/assets/font/font.css"
import VueTypedJs from 'vue-typed-js'

Vue.config.productionTip = false
Vue.use(VueTypedJs)

new Vue({
  render: h => h(index),
}).$mount('#app')


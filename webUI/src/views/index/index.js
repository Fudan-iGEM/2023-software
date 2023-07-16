import Vue from 'vue'
import index from './index.vue'
import "@/assets/font/font.css"

Vue.config.productionTip = false

new Vue({
  render: h => h(index),
}).$mount('#app')
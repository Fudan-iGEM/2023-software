import Vue from 'vue'
import home from './home.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.less'
import "@/assets/font/font.css"


Vue.config.productionTip = false
Vue.use(Antd);
new Vue({
    render: h => h(home),
}).$mount('#app')
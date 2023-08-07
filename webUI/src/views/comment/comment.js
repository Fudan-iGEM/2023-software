import Vue from 'vue'
import comment from './comment.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.less'
import '@/assets/font/font.css'
import VueDisqus from 'vue-disqus'



Vue.config.productionTip = false
Vue.use(Antd);
Vue.use(VueDisqus, {
    shortname: 'missyfield'
})

new Vue({
    render: h => h(comment),
}).$mount('#app')
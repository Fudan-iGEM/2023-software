import Vue from 'vue'
import reaction from './reaction.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.less'
import '@/assets/font/font.css'
import "vue-easytable/libs/theme-default/index.css";
import VueEasytable from "vue-easytable";
import { VeLocale } from "vue-easytable";
import enUS from "vue-easytable/libs/locale/lang/en-US.js";



Vue.config.productionTip = false
Vue.use(Antd);
Vue.use(VueEasytable);
VeLocale.use(enUS);


new Vue({
    render: h => h(reaction),
}).$mount('#app')
import {createApp, ref} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import Cookies from 'js-cookie';
import 'element-plus/dist/index.css'
import mitt from 'mitt';

export const eventBus = mitt();

// import ElementUI from 'element-ui';
// import 'element-ui/lib/theme-chalk/index.css';
const app = createApp(App);
//const isRefinery = ref(false);
const demoApi = ref('http://localhost:8082');
//ref('http://localhost:8082');
//ref('http://26.112.253.186:8082');
//ref('http://47.115.210.129:8082');
//app.provide('isRefinery', isRefinery);

app.provide('demoApi', demoApi);

//引入echarts
import * as echarts from 'echarts'

app.config.globalProperties.$echarts = echarts


app.use(ElementPlus).use(store).use(router).use(Cookies).mount('#app')

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import io from 'socket.io-client'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'


Vue.config.productionTip = false
Vue.use(Buefy)

var PulseLoader = require('vue-spinner/src/PulseLoader.vue');

new Vue({
    components: {
        'PulseLoader': PulseLoader
    },
  router,
  store,
  render: h => h(App)
}).$mount('#app')

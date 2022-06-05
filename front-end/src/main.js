import Vue from 'vue'
import App from './App.vue'
import VueRouter from "vue-router";
import Routes from "./routes";

Vue.use(VueRouter);

const rutas = new VueRouter({
  mode: "history",
	routes: Routes,
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
})

new Vue({
  el: '#app',
  render: h => h(App),
  router: rutas
})
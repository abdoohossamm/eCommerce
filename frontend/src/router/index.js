import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductView from "@/views/ProductView";
import CategoryView from "@/views/CategoryView";
import SearchView from "@/views/SearchView";
import CartView from "@/views/CartView";
import SignupView from "@/views/SignupView";
import LoginView from "@/views/LoginView";
import MyAccountView from "@/views/MyAccountView";
import store from "@/store";
import CheckoutView from "@/views/CheckoutView";
import SuccessView from "@/views/SuccessView";
import MyOrdersView from "@/views/MyOrdersView.vue";
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/product/:product_slug',
    name: 'product',
    component: ProductView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/my-account',
    name: 'my-account',
    component: MyAccountView,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/my-orders',
    name: 'my-orders',
    component: MyOrdersView,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/category/:category_slug',
    name: 'category',
    component: CategoryView
  },
  {
    path: '/cart',
    name: 'cart',
    component: CartView
  },
  {
    path: '/cart/checkout',
    name: 'checkout',
    component: CheckoutView,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/cart/success',
    name: 'success',
    component: SuccessView,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((to, from, next) =>{
  if(to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated){
    next({name:'login', query:{to: to.path}})
  }else {
    next()
  }
})
export default router

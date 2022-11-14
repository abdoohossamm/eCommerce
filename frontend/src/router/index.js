import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductView from "@/views/ProductView";
import CategoryView from "@/views/CategoryView";
import SearchView from "@/views/SearchView";
import CartView from "@/views/CartView";
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
    path: '/search',
    name: 'search',
    component: SearchView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

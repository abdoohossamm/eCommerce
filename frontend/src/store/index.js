import { createStore } from 'vuex'

export default createStore({
  state: {
    cart:{
      items:[],
    },
    isAuthenticated: false,
    token: '',
    isLoading: false
  },
  getters: {
  },
  mutations: {
    initializeStore(state){
      if (localStorage.getItem('cart')){
        state.cart = JSON.parse(localStorage.getItem('cart'))
      }else{
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }

      if (localStorage.getItem('token')){
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    addToCart(state, item){
      const exists = state.cart.items.filter(i => i.product.id === item.product.id)

      if (exists.length){
        exists[0].quantity = parseInt(exists[0].quantity + parseInt(item.quantity))
      }else{
        state.cart.items.push(item)
      }
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    setIsLoading(state, status){
      state.isLoading = status
    },
    clearCart(state){
      state.cart = {items: []}
      localStorage.setItem('cart', JSON.stringify(state.cart))

    }
  },
  actions: {
  },
  modules: {
  }
})

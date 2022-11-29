<template>
  <div class="page-my-account">
    <div class="column is-12">
      <h1 class="title">My orders</h1>
      <h3 class="subtitle"> You have successfully done {{count}} orders</h3>
    </div>
    <div class="section profile-heading">
      <div class="columns is-mobile is-multiline">
        <div class="column is-12">
          <OrderSummary
            v-for="order in orders"
            v-bind:key="order.id"
            v-bind:order="order"
          />
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import OrderSummary from "@/components/OrderSummary.vue"
export default {
  name: "MyOrdersView",
  components:{
    OrderSummary
  },
  data(){
    return{
      orders: [],
      count: 0,
      next: null,
      previous: null
    }
  },
  methods:{
    getMyOrders: async function(){
      this.$store.commit('setIsLoading', true)
      axios.get('/api/v1/orders/mine/')
          .then(response => {
            this.orders = response.data.results
            this.count = response.data.count
            this.next = response.data.next
            this.previous = response.data.previous
          }).catch(error => {
        console.log(error)
      })

      this.$store.commit('setIsLoading', false)
    }
  },
  mounted() {
    if (!axios.defaults.headers.common['Authorization']){
      this.$router.push("/login")
    }
    this.getMyOrders()
  }
}
</script>
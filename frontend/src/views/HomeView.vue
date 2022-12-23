<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">
          Welcome to eCommerce!
        </p>
        <p class="subtitle">
          The best online store.
        </p>
      </div>
    </section>
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2">Latest products</h2>
      </div>
      <ProductBox
          v-for="product in products"
          v-bind:key="product.id"
          v-bind:product="product"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductBox from "@/components/ProductBox";
export default {
  name: 'HomeView',
  data(){
    return {
      products:[]
    }
  },
  components: {
    ProductBox
  },
  mounted() {
    this.getProducts()
    document.title = "Home | eCommerce"
  },
  methods: {
    getProducts: async function(){
      this.$store.commit('setIsLoading', true)

      await axios.get('/api/v1/products').then(response =>{
        this.products = response.data.results
      }).catch(error =>{
        console.log(error)
      })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>

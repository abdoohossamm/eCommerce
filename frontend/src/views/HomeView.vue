<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">
          Welcome to eCommerce
        </p>
        <p class="subtitle">
          The best online store online
        </p>
      </div>
    </section>
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2">Latest products</h2>
      </div>
      <div
          class="column is-3"
          v-for="product in Products"
          v-bind:key="product.id"
      >
        <div class="box">
          <figure class="image mb-4">
            <img :src="product.thumbnail" alt="thumbnail for product">
          </figure>
          <h3 class="is-size-4">{{product.title}}</h3>
          <p class="is-size-6 has-text-grey-dark">{{product.price}}</p>
          <router-link v-bind:to="{name: 'product', params: {product_slug: product.slug}}" class="button is-dark mt-4">
            View details
          </router-link>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HomeView',
  data(){
    return {
      Products:[]
    }
  },
  components: {
  },
  mounted() {
    this.getProducts()
  },
  methods: {getProducts(){
    axios.get('/api/v1/products').then(response =>{
      this.Products = response.data.results
    }).catch(error =>{
      console.log(error)
    })
  }
  }
}
</script>

<style scoped>
  .image{
    margin-top: -1.25rem;
    margin-right: -1.25rem;
    margin-left: -1.25rem;
  }
</style>
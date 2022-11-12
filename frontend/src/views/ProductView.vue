<template>
  <div class="page-product">
    <div class="columns is-multiline">
      <div class="column is-9">
        <h1 class="title">{{product.title}}</h1>
        <figure class="image mb-6">
          <Carousel>
            <Slide v-for="(slide, id) in Slides" :key="id">
              <img :src="slide.image" alt="thumbnail for product">
            </Slide>

            <template #addons="{ slidesCount }">
              <Pagination/>
              <Navigation v-if="slidesCount > 1" />
            </template>
          </Carousel>
        </figure>
        <p>{{product.description}}</p>
      </div>
      <div class="column is-3">
        <h2 class="subtitle">Information</h2>
        <p><strong>Price: </strong>{{product.price}}</p>
        <div class="field has-addons mb-6">
          <div class="control">
            <input type="number" class="input" min="1" v-model="quantity">
          </div>
          <div class="control">
            <a class="button is-dark" @click="addToCart">Add to cart</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {toast} from "bulma-toast"
import 'vue3-carousel/dist/carousel.css';
import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel';
export default {
  name: "ProductView",
  data(){
    return{
      product:[],
      Slides:5,
      quantity: 1
    }
  },
  methods:{
     getProduct : async function (){
      this.$store.commit('setIsLoading', true)
      const product_slug = this.$route.params.product_slug

      await axios.get(`/api/v1/products/${product_slug}`).then(
          response => {
            this.product = response.data
            this.Slides = this.product.images
            document.title = this.product.title
          }
      ).catch( error =>{
        console.log(error)
      })
      this.$store.commit('setIsLoading', false)

    },
    addToCart: function (){
      if (isNaN(this.quantity) || this.quantity < 1){
        this.quantity = 1
      }
      const  item = {
        product: this.product,
        quantity: this.quantity
      }
      this.$store.commit('addToCart', item)
      toast(
          {
            message: 'The product was added to the cart',
            type: 'is-success',
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position:'bottom-center',
          }
      )
    }
  },
  mounted() {
    this.getProduct()
  },
  components: {
    Carousel,
    Slide,
    Pagination,
    Navigation,
  }
}


</script>

<style scoped>

</style>
<template>
  <div class="page-category">
    <h2 class="is-size-2 has-text-centered">{{category.name}}</h2>
    <div class="columns is-multiline">
      <ProductBox
          v-for="product in products"
          v-bind:key="product.id"
          v-bind:product="product"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {toast} from "bulma-toast";
import ProductBox from "@/components/ProductBox";
export default {
  name: 'CategoryView',
  data(){
    return{
      category:[],
      products:[]
  }
  },
  components:{
    ProductBox
  },
  mounted() {
    this.getCategory()
  },
  watch:{
    $route(to){
      if (to.name === "category"){
          this.getCategory()
      }
    }
  },
  methods:{
    getCategory: async function (){
      const categorySlug = this.$route.params.category_slug
      this.$store.commit('setIsLoading', true)
      await axios.get(`api/v1/categories/${categorySlug}/`).then(response =>{
        this.category = response.data.category
        this.products = response.data.products.results
        document.title = this.category.name

      }).catch(error =>{
        console.log(error)
        toast({
          message: 'Something went wrong, Please try again.',
          type: 'is-danger',
          dismissible:true,
          pauseOnHover:true,
          duration:2000,
          position:'bottom-right',
        })
      })
      this.$store.commit('setIsLoading', false)

    }
  }

}
</script>
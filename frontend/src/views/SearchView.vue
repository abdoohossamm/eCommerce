<template>
  <div class="page-search">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Search</h1>
        <h2 class="is-size-5 has-text-grey">
          Search term: "{{search}}"
        </h2>
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
import axios from "axios";
import ProductBox from "@/components/ProductBox";
import {toast} from "bulma-toast";
export default {
  name: "SearchView",
  components: {
    ProductBox
  },

  data(){
    return{
      products:[],
      search: ''
    }
  },
  mounted() {
    document.title = 'Search'
    let uri = window.location.search.substring(1)
    let params = new URLSearchParams(uri)

    if (params.get('search')){
      this.search = params.get('search')
      this.performSearch()
    }
  },
  methods:{
    performSearch: async function (){
      this.$store.commit('setIsLoading', true)

      await axios.get(`api/v1/products/?search=${this.search}`).then(response =>{
        this.products = response.data.results
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
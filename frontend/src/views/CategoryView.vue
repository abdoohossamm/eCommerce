<template>
  <div class="page-category">
    <h2 class="is-size-2 has-text-centered">{{category.name}}</h2>

  </div>
</template>

<script>
import axios from "axios";
import {toast} from "bulma-toast";
export default {
  name: 'CategoryView',
  data(){
    return{
      category:[],
      products:[]
  }
  },
  mounted() {
    this.getCategory()
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
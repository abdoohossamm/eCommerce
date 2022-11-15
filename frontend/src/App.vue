<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>eCommerce</strong></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
        <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu}">
          <div class="navbar-start">
            <router-link class="navbar-item" to="/">
              Home
            </router-link>

            <router-link class="navbar-item" to="/about">
              About
            </router-link>

            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                Categories
              </a>

              <div class="navbar-dropdown">
                  <router-link
                      v-for="category in Categories"
                      v-bind:key="category.slug"
                      v-bind:to="{
                        name: 'category',
                        params: {category_slug: category.slug}
                      }"
                     class="navbar-item"
                  >
                    {{category.name}}
                  </router-link>
              </div>
            </div>
            <div class="navbar-item">
              <form action="/search" method="get">
                <div class="field has-addons">
                  <div class="control">
                    <input type="text" class="input" placeholder="What are you looking for?" name="search">
                  </div>
                  <div class="control">
                    <button class="button is-success">
                      <span class="icon">
                        <i class="fas fa-search"></i>
                      </span>
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div class="navbar-end">
            <div class="navbar-item">
              <div class="buttons">
                <template v-if="$store.state.isAuthenticated">
                  <router-link to="/my-account" class="button is-light">My account</router-link>
                </template>
                <template v-else>
                <router-link to="/signup" class="button is-primary">Sign up</router-link>
                <router-link to="/login" class="button is-light">Log in</router-link>
                </template>
                <router-link to="/cart" class="button is-success">
                  <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                  <span>Cart ({{cartTotalLength}})</span>
                </router-link>
              </div>
            </div>
          </div>
        </div>
    </nav>
    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading}">
      <div class="lds-dual-ring">

      </div>
    </div>
    <section class="section">
    <router-view/>
    </section>
  </div>
  <footer class="footer">
    <p class="has-text-centered">Copyright Abdoohossamm (c) 2022</p>
  </footer>
</template>
<script>
import axios from "axios";

export default {
  data(){
    return{
      Categories: [],
      showMobileMenu: false,
      cart:{
        items:[]
      }
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token

    if (token){
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else{
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.cart = this.$store.state.cart
    axios.get('/api/v1/categories/').then(response =>{
      this.Categories = response.data.results
    }).catch(error =>{
      console.log(error)
    })
  },
  computed:{
    cartTotalLength(){
      let totalLength = 0
      for(let i=0; i<this.cart.items.length; i++){
        totalLength += this.cart.items[i].quantity
      }
      return totalLength
    }
  }
}
</script>
<style lang="scss">
@import "../node_modules/bulma";
.lds-dual-ring{
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after{
  content: ' ';
  display: block;
  width: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2ms linear infinite;
}
@keyframes lds-dual-ring {
  0%{
    transform: rotate(0deg);
  }
  100%{
    transform: rotate(360deg);
  }

}
.is-loading-bar{
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;

  &.is-loading{
    height: 80px;
  }
}
</style>

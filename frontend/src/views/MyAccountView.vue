<template>
  <div class="page-my-account">
    <div class="column is-12">
      <h1 class="title">My account</h1>
    </div>
    <div class="section profile-heading">
      <div class="columns is-mobile is-multiline">
        <div class="column is-2">
          <span class="header-icon user-profile-image">
            <img alt="" src="">
          </span>
        </div>
        <div class="column is-4-tablet is-10-mobile name">
          <p>
            <span class="title is-bold">{{user.first_name}} <span v-if="user.last_name"><br/> {{user.last_name}}</span></span>
            <br>
            <a class="button is-primary is-outlined" href="#" style="margin: 5px 0">
              Edit profile
            </a>
            <br/>
            <RouterLink to="/my-orders" class="button is-primary is-outlined" style="margin: 5px 0">My orders</RouterLink>
            <br>
          </p>
        </div>
        <template v-if="user.is_seller || user.is_staff">
          <div class="column is-2-tablet is-4-mobile has-text-centered">
            <p class="stat-val">30</p>
            <p class="stat-key">Products</p>
          </div>
          <div class="column is-2-tablet is-4-mobile has-text-centered">
            <p class="stat-val">10</p>
            <p class="stat-key">Reviews</p>
          </div>
          <div class="column is-2-tablet is-4-mobile has-text-centered">
            <p class="stat-val">5</p>
            <p class="stat-key">Sold</p>
          </div>
        </template>
      </div>
    </div>

    <div class="column is-12">
      <button @click="logout()" class="button is-danger">Log out</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyAccountView",
  data(){
    return{
      user: "",
    }
  },
  methods:{
    logout(){
      axios.defaults.headers.common["Authorization"] = ""
      localStorage.removeItem("token")
      localStorage.removeItem("username")
      localStorage.removeItem("userid")

      this.$store.commit("removeToken")
      this.$router.push('/')
    },
    getInfo: async function(){
      this.$store.commit('setIsLoading', true)
      axios.get('/api/v1/users/me/')
          .then(response =>{
            this.user = response.data
          }).catch(error=>{
        console.log(error)
      })

      this.$store.commit('setIsLoading', false)
    }
  },
  mounted() {
    if (!axios.defaults.headers.common['Authorization']){
      this.$router.push("/login")
    }
    this.getInfo()
  }
}
</script>

<style scoped>
body {
  background: #F5F7FA
}

.stat-val {
  font-size: 3em;
  padding-top: 20px;
  font-weight: bold;
}

.stat-key {
  font-size: 1.4em;
  font-weight: 200
}

.section.profile-heading .column.is-2-tablet.has-text-centered + .has-text-centered {
  border-left: 1px dotted rgba(0, 0, 0, .2);
}

.container.profile {
  margin-top: 1%;
}

.control.is-pulled-left span.select {
  margin-right: 5px;
  border-radius: 2px;
}

.modal-card .content h1 {
  padding: 40px 10px 10px;
  border-bottom: 1px solid #dadada
}

.container.profile .profile-options .tabs ul li.link a {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #F1F1F1;
}
</style>
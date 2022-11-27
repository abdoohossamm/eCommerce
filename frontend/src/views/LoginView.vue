<template>
  <div class="page-sign-up">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log in</h1>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label for="">Username or Email</label>
            <div class="control">
              <input type="text" placeholder="Please enter your username or email"
                     class="input" id="email-input" v-model="username"
              >
            </div>
          </div>
          <div class="field">
            <label for="">Password</label>
            <div class="control">
              <input type="password" placeholder="Please enter your password" class="input" id="password-input" v-model="password">
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{error}}</p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-dark">Log in</button>
            </div>
          </div>
          <hr>
          <p>Or <router-link to="/signup">Click Here</router-link> to Sign up!</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script >
import axios from "axios";
export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      errors: []
    }
  },mounted() {
    document.title = "Login"

  },
  methods:{
    submitForm: async function(){
      axios.defaults.headers.common["Authorization"] = ""

      localStorage.removeItem('token')
      const formData = {
        username: this.username,
        password: this.password
      }
      await axios
          .post('api/v1/token/login', formData)
          .then(response =>{
            const token = response.data.auth_token
            this.$store.commit('setToken', token)
            axios.defaults.headers.common['Authorization'] = "Token " + token
            localStorage.setItem('token', token)
            const toPath = this.$route.query.to || '/cart'
            this.$router.push(toPath)
          })
          .catch(error =>{
            if (error.response){
              for(const property in error.response.data){
                this.errors.push(
                    `${property.charAt(0).toUpperCase() + property.slice(1)}: ${error.response.data[property]}`
                )
                document.getElementById(`${property}-input`).setAttribute('class', 'input is-danger')
              }
              console.log(JSON.stringify(error.response.data))
            }else if(error.message){
              this.errors.push(`Something went wrong, Please try again`)
              console.log(JSON.stringify(error))
            }
          })
    }
  }
}
</script>
<template>
  <div class="page-sign-up">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Sign up</h1>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label for="">Username</label>
            <div class="control">
              <input type="text" class="input" id="username-input" v-model="username">
            </div>
          </div>
          <div class="field">
            <label for="">Email</label>
            <div class="control">
              <input type="email" class="input" id="email-input" v-model="email">
            </div>
          </div>
          <div class="field">
            <label for="">Password</label>
            <div class="control">
              <input type="password" class="input" id="password-input" v-model="password">
            </div>
          </div>

          <div class="field">
            <label for="">Repeat password</label>
            <div class="control">
              <input type="password" class="input" id="password2-input" v-model="password2">
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{error}}</p>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-dark">Sign up</button>
            </div>
          </div>
          <hr>
          <p>Or <router-link to="/login">Click Here</router-link> to log in!</p>
        </form>
      </div>
    </div>
  </div>
</template>
<script>

import axios from "axios";
import {toast} from "bulma-toast";

export default {
  name: 'SignupView',
  data() {
    return{
      username: '',
      email:'',
      password: '',
      password2: '',
      errors: []
    }
  },
  methods:{
    submitForm: function (){
      this.errors = []
      if (this.username === ''){
        this.errors.push('The username is missing')
        document.getElementById('username-input').setAttribute('class', 'input is-danger')
      }
      if(this.email === ''){
        this.errors.push('The email is missing')
        document.getElementById('email-input').setAttribute('class', 'input is-danger')
      }
      if(this.password === ''){
        this.errors.push('The password is too short')
        document.getElementById('password-input').setAttribute('class', 'input is-danger')
      }
      if(this.password2 !== this.password){
        this.errors.push("The passwords doesn't match")
        document.getElementById('password-input').setAttribute('class', 'input is-danger')
        document.getElementById('password2-input').setAttribute('class', 'input is-danger')
      }
      if(!this.errors.length){
        const formData = {
          username: this.username,
          email: this.email,
          password: this.password,
        }
        axios
            .post('/api/v1/users/', formData)
            .then(response =>{
              console.log(response)
              console.log('response done')
              toast({
                message: 'Account created, please log in!',
                type:'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration:2000,
                position: "bottom-right",
              })
                this.$router.push('/login')
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
            }
        )

      }
    },
  }
}
</script>
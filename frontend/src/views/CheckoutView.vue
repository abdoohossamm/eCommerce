<template>
  <div class="page-checkout">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Checkout</h1>
      </div>
      <div class="column is-12 box">
        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Total</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in cart.items"
              v-bind:key="item.product.id"
            >
              <td>{{item.product.title}}</td>
              <td>{{item.product.price}}</td>
              <td>{{item.quantity}}</td>
              <td>{{getItemTotal(item).toFixed(2)}}</td>

            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="2">Total</td>
              <td >{{cartTotalLength}}</td>
              <td >{{cartTotalPrice.toFixed(2)}}</td>
            </tr>
          </tfoot>
        </table>
      </div>
      <div class="column is-12 box">
        <h2 class="subtitle">Shipping details</h2>
        <p class="has-text-grey mb-4">* All fields are required</p>
        <div class="columns is-multiline">
          <div class="column is-6">
            <div class="field">
              <label for="">First name*</label>
              <div class="control">
                <input id='first_name-input' type="text" class="input" v-model="first_name">
              </div>
            </div>

            <div class="field">
              <label for="">Last name*</label>
              <div class="control">
                <input id='last_name-input' type="text" class="input" v-model="last_name">
              </div>
            </div>

            <div class="field">
              <label for="">E-mail*</label>
              <div class="control">
                <input id='email-input' type="email" class="input" v-model="email">
              </div>
            </div>

            <div class="field">
              <label for="">Phone*</label>
              <div class="control">
                <input id='phone-input' type="text" class="input" v-model="phone">
              </div>
            </div>

          </div>
          <div class="column is-6">
            <div class="field">
              <label for="">Address*</label>
              <div class="control">
                <input id='address-input' type="text" class="input" v-model="address">
              </div>
            </div>

            <div class="field">
              <label for="">Zip code</label>
              <div class="control">
                <input id='zipcode-input' type="number" class="input" v-model="zipcode">
              </div>
            </div>

            <div class="field">
              <label for="">Place*</label>
              <div class="control">
                <input id='place-input' type="text" class="input" v-model="place">
              </div>
            </div>
          </div>
        </div>
          <fieldset>
            <legend>Select a Payment method:</legend>
            <div>
              <input type="radio" id="online" name="payment_method" value="online" v-model="payment_method" @click="setThePayment">
              <label for="online">Online payment</label>
            </div>

            <div>
              <input type="radio" id="cash" name="payment_method" value="cash" v-model="payment_method" @click="setThePayment">
              <label for="cash">Cash on delivery (+10 USD)</label>
            </div>
          </fieldset>
        <hr>
        <div class="notification is-danger mt-4" v-if="errors.length">
          <p v-for="error in errors" v-bind:key="error">{{error}}</p>
        </div>

        <div id="card-element" class="mb-5">
          <template v-if="cartTotalLength">
            <button id="pay-now" class="button is-dark" @click="submitForm">Pay now!</button>
          </template>
        </div>
        <div id="payment-card" class="mb-5">
          <div id="paypal-button-container"></div>

        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from "axios";
export default {
  name:"CheckoutView",
  data(){
    return{
      cart:{
        items:[]
      },
      paypal:{},
      card:{},
      first_name:"",
      last_name:"",
      email:"",
      phone:"",
      address:"",
      zipcode: null,
      place:"",
      cash_on_delivery: false,
      errors: [],
    }
  },
  mounted() {
    document.title = "Checkout"
    this.cart = this.$store.state.cart

  },
  methods: {
    getItemTotal(item){
      return item.quantity * item.product.price
    },
    submitForm(){
      this.errors = []
      if (this.first_name === ''){
        this.errors.push('The first name field is missing!')
        document.getElementById('first_name-input').setAttribute('class', 'input is-danger')
      }
      if (this.last_name === ''){
        this.errors.push('The last name field is missing!')
        document.getElementById('last_name-input').setAttribute('class', 'input is-danger')

      }
      if (this.email === ''){
        this.errors.push('The email field is missing!')
        document.getElementById('email-input').setAttribute('class', 'input is-danger')

      }
      if (this.phone === ''){
        this.errors.push('The email field is missing!')
        document.getElementById('phone-input').setAttribute('class', 'input is-danger')

      }
      if (this.address === ''){
        this.errors.push('The address field is missing!')
        document.getElementById('address-input').setAttribute('class', 'input is-danger')
      }
      if (this.place === ''){
        this.errors.push('The place field is missing')
        document.getElementById('place-input').setAttribute('class', 'input is-danger')
      }
      if (this.errors.length === 0){
        document.getElementById('pay-now').disabled=true
        document.getElementById('first_name-input').disabled=true
        document.getElementById('last_name-input').disabled=true
        document.getElementById('email-input').disabled=true
        document.getElementById('phone-input').disabled=true
        document.getElementById('address-input').disabled=true
        document.getElementById('place-input').disabled=true
        document.getElementById('online').disabled=true
        document.getElementById('cash').disabled=true
      }
      if (!this.errors.length){
        this.submitData()
      }
    },
    setThePayment: function (){
      if (document.getElementById("online").checked){
        document.getElementById('pay-now').innerHTML = "Pay now!"
        this.cash_on_delivery = false
      }
      else if (document.getElementById("cash").checked){
        document.getElementById('pay-now').innerHTML = "Pay later!"
        this.cash_on_delivery = true
      }
    },
    submitData: async function(){
      const items = []
      for(let i=0; i<this.cart.items.length; i++){
        const item = this.cart.items[i]
        const obj = {
          product: item.product.id,
          quantity: item.quantity,
          price: item.product.price
        }
        items.push(obj)
      }
      const formData = {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        zipcode: this.zipcode,
        address: this.address,
        place: this.place,
        phone: this.phone,
        return_url: `${window.location.origin}/cart/success/`,
        cancel_url: document.URL,
        cash_on_delivery: this.cash_on_delivery,
        items: items
      }
      this.$store.commit('setIsLoading', true)
      await axios.
      post('/api/v1/orders/', formData)
          .then(response => {
            if(response.data.paypal){
              const data = response.data
              window.open(data.paypal[0].links[1].href)
            }

          }).catch(errors =>{
            console.log(errors)
          }
      )
      this.$store.commit('setIsLoading', false)
    }
  },
  computed:{
    cartTotalLength: function () {
      return this.cart.items.reduce((acc, curVal) => {
        return acc + curVal.quantity
      }, 0)
    },
    cartTotalPrice: function () {
      return this.cart.items.reduce((acc, curVal) => {
        return acc + curVal.quantity * curVal.product.price
      }, 0)
    },
  },
}
</script>
<template>
  <div class="page-success">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 id="title" class="title">Checking the payment ....</h1>
        <h2 id="sub-title" class="is-size-5 has-text-grey">
          Please wait....!
        </h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SuccessView",
  data(){
    return{
      token: ''
    }
  },
  mounted() {
    document.title = 'Order success'
    let uri = window.location.search.substring(1)
    let params = new URLSearchParams(uri)

    if (params.get('token')){
      this.token = params.get('token')
      this.capturePayment()
    }
  },
  methods:{
    capturePayment: async function (){
      const formData = {
        token: this.token
      }
      this.$store.commit('setIsLoading', true)
      await axios.
      post('/api/v1/orders/capture/', formData)
          .then(response => {
              this.status = response.data.status
            if (this.status === 'COMPLETED'){
                document.getElementById('title').innerHTML = "Thank you for buying from us"
                document.getElementById("sub-title").innerHTML = "Your order will be processed within 48 hours"
                this.$store.commit('clearCart')
            }
            else if (this.status === "ORDER_ALREADY_CAPTURED"){
              document.getElementById("title").innerHTML = "We are processing your order please wait!"
              document.getElementById("sub-title").innerHTML = "You can reach us by calling the customer service"
            }
            else if (this.status === "ORDER_NOT_APPROVED"){
              document.getElementById("title").innerHTML = "This ordered isn't paid yet, please pay in less than 7 days of ordering or the order will be deleted"
              document.getElementById("sub-title").innerHTML = "If you have any problem please reach our customer service"
            }
          }).catch(errors =>{
            console.log(errors)
                if (errors.response.status === 404){
                  document.getElementById("title").innerHTML = "We couldn't find your order"
                  document.getElementById("sub-title").innerHTML = "If you have any problem please reach our customer service"

                }
                else {
                  document.getElementById("title").innerHTML = "Unknown error happened Please contact the customer service"
                  document.getElementById("sub-title").innerHTML = ""
                }
              }
          )
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>
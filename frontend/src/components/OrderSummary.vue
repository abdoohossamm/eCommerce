<template>
  <div class="box mb-4">
    <h3 class="is-size-4 mb-1">
      Order #{{order.payment_token}} <span v-if="order.delivered" class="has-text-success pl-4"> Delivered</span>
      <span v-else class="has-text-danger pl-4">Not delivered yet</span>
    </h3>
    <h3 class="is-size-5 mb-5">
      <router-link
          v-bind:to="{
          name: 'order',
          params: {order_id: order.payment_token}
        }"

      >
        view details
      </router-link>
    </h3>


    <h4 class="is-size-5">Products</h4>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th >Product</th>
          <th>Price</th>
          <th>Quantity</th>
          <th>Total</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="item in order.items"
          v-bind:key="item.product.id"
        >

          <td>
            <router-link
                v-bind:to="{
                name: 'product',
                params: {product_slug: item.product.slug}
                }"
            >
            <img v-bind:src="item.product.thumbnail" alt="product thumbnail" width="80" height="80"/>
            <br/>
            <strong class="mb-8 is-size-6">{{item.product.title}}</strong>
              </router-link>
          </td>
          <td>{{item.product.price}}</td>
          <td>{{item.quantity}}</td>
          <td>{{getItemTotal(item).toFixed(2)}}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="2">Total</td>
          <td >{{orderTotalLength(order)}}</td>
          <td >{{orderTotalPrice().toFixed(2)}}</td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script>
export default {
  name:"OrderSummary",
  props:{
    order:Object
  },
  methods:{
    getItemTotal(item){
      return item.quantity * item.product.price
    },
    orderTotalLength(order){
      return order.items.reduce((acc, curVal) => {
        return acc + curVal.quantity
      }, 0)
    },
    orderTotalPrice: function () {
      return this.order.items.reduce((acc, curVal) => {
        return acc + curVal.quantity * curVal.product.price
      }, 0)
    }
  }
}
</script>

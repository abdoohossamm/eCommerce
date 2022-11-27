<template>
  <div class="column is-3">
    <div class="box">
      <figure class="image mb-4">
        <img :src="product.thumbnail" alt="thumbnail for product">
      </figure>
      <h3 class="is-size-4">{{product.title}}</h3>
      <p class="is-size-6 has-text-grey-dark">{{product.price}}</p>
      <router-link
          v-bind:to="{name: 'product',
                      params: {product_slug: product.slug}}"
          class="button is-dark mt-4"
      >
        View details
      </router-link>

    </div>
  </div>
</template>
<script>
export default {
  name: 'ProductBox',
  props:{
    product:Object
  }
}
</script>
<style scoped>
.image{
  margin-top: -1.25rem;
  margin-right: -1.25rem;
  margin-left: -1.25rem;
}
img {
  width: 400px;
  height: 300px;
}
</style>
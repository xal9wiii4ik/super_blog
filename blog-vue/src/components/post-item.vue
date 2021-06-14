<template>
  <div class="post">
    <div class="post__items">
      <div class="post__left">
        <img :src="`${post.image}`" class="post__image"/>
      </div>
      <div class="post_right">

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "post-item",
  props: {
    post: {
      type: Object,
      required: true,
      default: () => {
      },
    }
  }
}
</script>

<style scoped>

</style>
<template>
  <div class="post__items">
    <img :src="`${post.image}`" class="post__image"/>
    <div class="post__content">
      <div class="post__content__txt">
        <h4 class="post__title">{{ post.title }}</h4>
        <h4 class="post__description">{{ post.description }}</h4>
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
.post__items {
  position: relative;
  overflow: hidden;
  height: 300px;
}

.post__image {
  position: absolute;
  left: 50%;
  top: 50%;
  z-index: -1;
  transform: translate3d(-50%, -50%, 0);
}

.post__items:hover .post__content {
  opacity: 1;
}

.post__content {
  display: flex;
  position: absolute;
  flex-direction: column;
  text-align: left;
  opacity: 0;
  width: 100%;
  height: 100%;
  top: auto;
  z-index: 2;
  transition: .2s;
  bottom: auto;
}

.post__content__txt {
  background-color: rgba(192, 192, 192, .4);
  /*position: absolute;*/
}

.post__title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 10px;
}

.post__description {
  font-size: 14px;
}
</style>
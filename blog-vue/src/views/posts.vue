<template>
  <div class="container">
    <post-item
          v-for="post in posts"
          v-bind:key="post.id"
          v-bind:post="post">
    </post-item>
  </div>
</template>

<script>
import postItem from '@/components/post-item';
export default {
  name: 'posts',
  data() {
    return {
      posts: []
    }
  },
  components: {'post-item': postItem},
  mounted() {
    this.get_posts()
  },
  methods: {
    async get_posts() {
      const response = await fetch('http://127.0.0.1:8000/api/posts/', {
        method: 'GET',
      })
      if (response.status === 200) {
        this.posts = await response.json()
      }else{
        console.log('not found')
      }
    }
  },
}
</script>
<style scoped lang="scss">
</style>
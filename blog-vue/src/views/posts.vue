<template>
  <div class="container">
    {{posts}}
  </div>
</template>

<script>
export default {
  name: 'posts',
  data() {},
  mounted() {
    this.get_posts()
  },
  methods: {
    async get_posts() {
      const response = await fetch('http://127.0.0.1:8000/posts/', {
        method: 'GET',
      })
      if (response.status === 200) {
        this.rooms = await response.json()

      }else{
        console.log('not found')
      }
    }
  },
}
</script>
<style scoped lang="scss">
</style>
<template>
  <div class="container">
    <form class="login__form" @submit.prevent="submitForgotPasswordHandler">
      <label for="images" class="chose">Chose the files</label>
      <input type="file" id="images" ref="files" @change="onFileSelected" multiple class="login__form__input__images">
      <span v-if="file">{{file.name}}</span>
      <div v-for="(file, index) in files" :key=index class="level">
        <div class="level-left">
          <div class="level-item">{{file.name}}</div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <a @click.prevent="files.splice(index, 1)" class="delete">delete</a>
          </div>
        </div>
      </div>
      <button class="login__form__button">submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "check",
  data() {
    return {
      files: [],
      file: null
    }
  },
  methods: {
    async onFileSelected(event) {
      const files = this.$refs.files.files
      this.files = [ ...this.files, ...files ]
      console.log(this.files)
    },
    async submitForgotPasswordHandler() {
      console.log(this.files)
    }
  }
}
</script>

<style scoped>

.chose {
    width: 180px;
    height: 50px;
    border-radius: 4px;
    text-align: center;
    margin: 25px;
    cursor: pointer;
    display: block;
    font: 14px/50px Tahoma;
    transition: all 0.18s ease-in-out;
    border: 1px solid #4FD666;
    background: linear-gradient(to top right, #3EC97A, #69EA49 20%, rgba(255, 255, 255, 0) 80%, rgba(255, 255, 255, 0)) top right/500% 500%;
    color: #4FD666;
}

.chose:hover {
    color: white;
    background-position: bottom left;
}

.login__form__input__images {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}

.level {
  display: flex;
  flex-direction: row;
}

.level-left {
  display: flex;
  flex-direction: column;
  justify-content: left;
  align-items: flex-start;
}

.level-item {
  font-size: 15px;
}

.delete {
  color: red;
  cursor: pointer;
}
</style>
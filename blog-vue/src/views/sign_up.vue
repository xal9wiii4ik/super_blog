<template>
  <div class="container">
    <pre class="pre" v-if="is_submit">
    </pre>
    <div class="login">
      <h4 class="login__title">sign up</h4>
      <form class="login__form" @submit.prevent="submitForgotPasswordHandler">
        <h5 class="login__form__input__title">Enter email*</h5>
        <input type="email" v-model="email" required class="login__form__input">
        <h5 class="login__form__input__title">Enter username*</h5>
        <input type="text" v-model="username" required class="login__form__input">
        <h5 class="login__form__input__title">Enter first_name*</h5>
        <input type="text" v-model="first_name" required class="login__form__input">
        <h5 class="login__form__input__title">Enter last_name*</h5>
        <input type="text" v-model="last_name" required class="login__form__input">
        <h5 class="login__form__input__title">Enter your telegram chat id</h5>
        <input type="text" v-model="telegram_chat_id" class="login__form__input">
        <h5 class="login__form__input__title">Enter your phone*</h5>
        <input type="text" v-model="phone" required class="login__form__input">
        <h5 class="login__form__input__title">Select gender*</h5>
        <select id="selected" name="select-gender" v-model="gender" required class="login__form__input">
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
        <h5 class="login__form__input__title">Enter password*</h5>
        <input type="password" v-model="password" required class="login__form__input">
        <h5 class="login__form__input__title">Enter repeat password*</h5>
        <input type="password" v-model="repeat_password" required class="login__form__input">
        <h5 class="login__form__input__title">Choose images*</h5>
        <label for="files" class="chose">Chose the files</label>
        <input type="file" id="files" ref="images" @change="onImageSelected" multiple required
               class="login__form__input__images">
        <div v-for="(image, index) in images" :key=index class="level">
          <div class="level-left">
            <div class="level-item">{{ image.name }}</div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <a @click.prevent="images.splice(index, 1)" class="delete">delete</a>
            </div>
          </div>
        </div>
        <button class="login__form__button">submit</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "sign_up",
  data() {
    return {
      email: '',
      password: '',
      repeat_password: '',
      username: '',
      first_name: '',
      last_name: '',
      phone: '',
      gender: '',
      telegram_chat_id: '',
      is_submit: false,
      images: [],
      image: null
    }
  },
  methods: {
    async onImageSelected() {
      const images = this.$refs.images.files
      this.images = images
    },
    async submitForgotPasswordHandler() {
      try {
        this.is_submit = true
        const data = {
          email: this.email,
          password: this.password,
          repeat_password: this.repeat_password,
          username: this.username,
          first_name: this.first_name,
          last_name: this.last_name,
          gender: this.gender,
          phone: this.phone,
          image: this.images[0]
        }
        if (this.telegram_chat_id !== '') {
          data['telegram_chat_id'] = this.telegram_chat_id
        }
        const formData = new FormData();
        for (const name in data) {
          console.log(name)
          console.log(data[name])
          formData.append(name, data[name]);
        }
        const response = await fetch('http://0.0.0.0:8000/api/account/', {
          method: 'POST',
          body: formData
        });
        const response_data = await response.json()
        var poemDisplay = document.querySelector('pre');
        if (response.status === 200) {
          console.log(response_data)
          poemDisplay.textContent = Object.values('All is good, check your email')
          poemDisplay.style.color = 'chartreuse'
        } else {
          poemDisplay.textContent = Object.values(response_data)
          poemDisplay.style.color = 'red'
        }
      } catch (e) {
        alert(e)
      }
    }
  }
}
</script>

<style scoped>

.container {
  position: absolute;
  justify-content: center;
  display: flex;
  align-items: center;
  flex-direction: column;
}

.pre {
  padding-top: 30px;
  padding-bottom: 30px;
  font-size: 20px;
}

.login {
  width: 45%;
  border-radius: 20px;
  border: 1px solid darkblue;
}


.login__title {
  padding: 40px 20px;
  text-transform: uppercase;
  font-size: 20px;
}

.login__form {
  display: flex;
  flex-direction: column;
  padding: 30px 20px;
}

.login__form__input__title {
  text-transform: uppercase;
  font-size: 15px;
}

.login__form__input {
  padding: 10px 60px;
  width: 70%;
  margin: 10px auto;
  color: black;
  border-radius: 100px;
  border: none;
}

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

.login__form__button {
  color: black;
  text-transform: uppercase;
  margin: 25px auto;
  padding: 10px 100px;
  border: 1px solid aqua;
}

.level {
  display: flex;
  flex-direction: row;
  margin: 0;
}

.level-left {
  display: flex;
  flex-direction: column;
  justify-content: left;
  align-items: flex-start;
  margin: 0;
}

.level-right {
  display: flex;
  flex-direction: column;
  justify-content: right;
  align-items: flex-end;
  margin-right: 0;
}

.level-item {
  font-size: 15px;
}

.delete {
  color: red;
  cursor: pointer;
}
</style>
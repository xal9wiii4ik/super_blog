<template>
  <div class="container">
    <pre class="pre" v-if="is_submit">
    </pre>
    <div class="login">
      <h4 class="login__title">login</h4>
      <form class="login__form" @submit.prevent="submitForgotPasswordHandler">
        <h5 class="login__form__input__title">Enter email</h5>
        <input type="text" v-model="email" required class="login__form__input">
        <h5 class="login__form__input__title">Enter password</h5>
        <input type="password" v-model="password" required class="login__form__input">
        <h5 class="login__form__input__title">Enter repeat password</h5>
        <input type="password" v-model="repeat_password" required class="login__form__input">
        <button class="login__form__button">submit</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "forgot_password",
  data() {
    return {
      email: '',
      password: '',
      repeat_password: '',
      is_submit: false
    }
  },
  methods: {
    async submitForgotPasswordHandler() {
      try {
        this.is_submit = true
        const data = {
          email: this.email,
          password: this.password,
          repeat_password: this.repeat_password
        }
        const response = await fetch('http://0.0.0.0:8000/api/account/reset_password/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        const response_data = await response.json()
        const poemDisplay = document.querySelector('pre');
        if (response.status === 200) {
          console.log(response_data)
          poemDisplay.textContent = Object.values(response_data)
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
}

.login__form__button {
  color: black;
  text-transform: uppercase;
  margin: 25px auto;
  padding: 10px 100px;
  border: 1px solid aqua;
}
</style>
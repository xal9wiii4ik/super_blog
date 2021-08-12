<template>
  <div class="container">
    <div class="login">
      <h4 class="login__title">login</h4>
      <form class="login__form" @submit.prevent="submitLoginHandler">
        <h5 class="login__form__input__title">Enter username or email</h5>
        <input type="text" v-model="username_or_email" class="login__form__input">
        <h5 class="login__form__input__title">Enter password</h5>
        <input type="password" v-model="password" class="login__form__input">
        <button class="login__form__button">login</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      username_or_email: '',
      password: ''
    }
  },
  methods: {
    async submitLoginHandler() {
      try {
        if (this.username_or_email.indexOf('@') > -1) {
          var data = {
            email: this.username_or_email,
            password: this.password
          }
        } else {
          var data = {
            username: this.username_or_email,
            password: this.password
          }
        }
        const response = await fetch('http://0.0.0.0:8000/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
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
}

.login {
  width: 45%;
  border-radius: 20px;
  border: 1px solid;
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
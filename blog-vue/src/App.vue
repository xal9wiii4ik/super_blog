<template>
  <div class="nav">
    <div class="nav__items">
      <nav class="header__nav">
        <ul class="header__list">
          <li class="header__list__item">
            <router-link class="header__list__link" to="/">
              <h4 class="header__list__link">home</h4>
            </router-link>
          </li>
          <li class="header__list__item">
            <router-link class="header__list__link" to="/posts/">
              <h4 class="header__list__link">posts</h4>
            </router-link>
          </li>
          <li class="header__list__item" v-if="!is_authorized">
            <router-link class="header__list__link" to="/login/">
              <h4 class="header__list__link">login</h4>
            </router-link>
          </li>
          <li class="header__list__item" v-if="!is_authorized">
            <router-link class="header__list__link" to="/sign_up/">
              <h4 class="header__list__link">sign up</h4>
            </router-link>
          </li>
          <li class="header__list__item" v-if="is_authorized">
            <router-link class="header__list__link" to="/">
              <h4 class="header__list__link">{{ this.username }}</h4>
            </router-link>
          </li>
          <li class="header__list__item" v-if="is_authorized">
            <router-link class="header__list__link" to="/" v-on:click="logout">
              <h4 class="header__list__link">logout</h4>
            </router-link>
          </li>
        </ul>
      </nav>
    </div>
  </div>
  <router-view/>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      is_authorized: false,
      username: '',
      user_id: '',
    }
  },
  async mounted() {
    await this.getUserInfo()
  },
  methods: {
    async getUserInfo() {
      if (localStorage.getItem('access_token')) {
        this.is_authorized = true
        this.user_id = localStorage.getItem('user_id')
        this.username = localStorage.getItem('username')
      } else {
        this.is_authorized = false
      }
    },
    async logout() {
      localStorage.clear()
      this.is_authorized = false
    }
  },
}
</script>

<style>

input::placeholder {
  color: white;
  font-style: italic;
}

html {
  scroll-behavior: smooth;
  overflow-x: hidden;
  width: 100%;
  height: 100%;
}

* {
  padding: 0;
  margin: 0 auto;
  box-sizing: border-box;
  font-family: sans-serif;
}

body {
  min-height: 100vh;
  overflow-x: hidden;
  background-color: #F5F5F5;
}

a {
  text-decoration: none;
}

.container {
  width: 100%;
  height: 100%;
  margin: 0 auto;
  text-align: center;
}

button {
  text-decoration: none;
  cursor: pointer;
  border: none;
  color: white;
  border-radius: 100px;
  background-color: white;
  padding: 15px;
  text-align: center;
  margin-left: 10px;
  font-size: 15px;
}

input {
  text-decoration: none;
  text-align: center;
  border-radius: 100px;
  border: none;
  outline: none;
}

input::placeholder {
  color: white;
  font-style: italic;
}

.nav__items {
  width: 60%;
}

.nav {
  padding-top: 15px;
  padding-bottom: 15px;
  background-color: white;
}

.nav a {
  font-weight: bold;
  color: #2c3e50;
}

.nav a.router-link-exact-active {
  color: #42b983;
}

.header__nav {
  width: 100%;
  text-transform: uppercase;
  padding: 5px;
}

.header__list {
  list-style-type: none;
  text-decoration: none;
  display: flex;
  flex-direction: row;
  text-align: center;
  justify-content: center;
}

.header__list__item {
  padding-left: 40px;
}

.header__list__link {
  color: black;
  text-transform: uppercase;
  font-size: 15px;
}
</style>


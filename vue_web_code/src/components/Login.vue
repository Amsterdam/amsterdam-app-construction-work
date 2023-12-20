<template>
  <div>
    <div class="card login" @submit="login">
      <div>
        <div style="text-align: left">
          <a class="mainlogo" href="https://www.amsterdam.nl">
            <img src="@/assets/logo.svg" alt="Gemeente Amsterdam" />
          </a>
        </div>
        <div class="spacer" />
      </div>
      <form>
        <div class="align-left margin-less">
          <span class="align-left" style="font-weight: 600; color: darkgray">
            Voer uw gebruikersnaam in
          </span>
        </div>
        <b-field :type="message ? 'is-danger' : 'is-primary'">
          <b-input v-model="username" />
        </b-field>
        <div class="align-left margin-less">
          <span class="align-left" style="font-weight: 600; color: darkgrey">
            Voer uw wachtwoord in
          </span>
        </div>
        <b-field :type="message ? 'is-danger' : 'is-primary'">
          <b-input v-model="password" type="password" />
        </b-field>
        <b-button native-type="submit" type="is-primary">
          <b-icon icon="sign-in-alt" pack="fas" />
          <span style="font-weight: 600">Aanmelden</span>
        </b-button>
      </form>
    </div>
  </div>
</template>

<script>
import { getTokenUrl } from '@/api'
import axios from 'axios'
export default {
  name: 'login-component',
  data() {
    return {
      username: 'communicare@amsterdam.nl',
      password: 'Kl31nDu1mpj3',
      message: '',
    }
  },
  methods: {
    async login(e) {
      e.preventDefault()
      let data = {
        username: this.username,
        password: this.password,
      }

      axios
        .post(getTokenUrl, data)
        .then((response) => {
          if (response.data.error) {
            this.message = JSON.stringify(response.data.error)
          } else {
            axios.defaults.headers.common['Authorization'] = response.data.access
            this.$store.commit('login', {
              refresh: response.data.refresh,
              access: response.data.access,
              username: data.username,
            })
          }
          this.$router.push('/')
        })
        .catch((err) => {
          console.log(err)
          this.message = `${err.status}: ${err.statusText}`
        })
    },
  },
}
</script>

<style>
.spacer {
  margin: 15px;
}

.margin-less {
  margin: 0;
  padding: 0;
}

.login {
  flex-grow: 1;
  margin: 0 auto;
  position: relative;
  width: 600px;
}

body {
  background-image: url('/src/assets/background.jpg');
  background-size: cover;
  min-width: 100%;
  background-repeat: no-repeat;
  background-position: center center;
}
</style>
